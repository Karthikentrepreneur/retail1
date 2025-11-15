# Key Flows

## POS Sale (Online)
1. **Cashier scans items** via POS UI which calls `GET /products?query=` and caches SKUs locally. Variant and tax metadata pulled from backend.
2. **Cart totals** computed client-side and validated via `POST /sales` with payload containing tenant + store scopes. Backend service verifies tenant context, calculates tax via rules engine, persists sale and items, and triggers stock ledger updates in a transaction.
3. **Payment selection**: if UPI or PG is chosen, `POST /pg/order` creates a Razorpay order; the response includes QR/link. POS subscribes to WebSocket/SSE for payment status.
4. **Webhook handling**: PG posts to `/pg/webhook` with idempotency key. Backend validates signature, updates `payments` row, sets sale `payment_status=success`, and enqueues receipt printing event.
5. **Receipt printing**: POS calls `POST /sales/{id}/print` to fetch ESC/POS template. Cloud Storage stores PDF/A4 invoice; email dispatch handled via async job.
6. **GST (optional)**: if tenant has GST suite, `gst_worker` is triggered with sale ID. Worker formats payload, sends to GSP, stores IRN/QR, and updates `gst_documents`.

## POS Sale (Offline Android)
1. Device syncs catalog snapshot and stock to SQLite using `/sync/pull` before offline period.
2. Sales executed locally using device invoice series `DEV-<device_id>-counter`. Stock decremented locally with optimistic locking.
3. On connectivity restore, app pushes queued operations via `/sync/push` with idempotency keys. Server validates stock, reassigns invoice number from master sequence, recalculates tax, and may mark sale `needs_review` if conflicts.
4. Server returns final invoice, IRN (if applicable), and updated stock, which app persists. Any conflicts raise alerts in tenant admin dashboard.

## Purchase & GRN
1. Manager raises PO via `/purchase-orders` (future endpoint) referencing supplier and warehouse. Status transitions to `issued`.
2. At receipt, GRN captures batch info via `/grns`. Stock ledger increments FIFO layers, inventory balances updated per batch.
3. Supplier invoice recorded linking GRN lines. Payments to suppliers tracked via `/payments` with `supplier_invoice_id` scope.
4. AP aging report aggregates open invoices and due dates.

## E-invoice & E-waybill
1. Worker polls `gst_documents` table for `pending` records or processes Pub/Sub message.
2. Payload assembled per NIC schema, signed, and submitted to chosen GSP adapter. Success response persists IRN, AckNo, QR JSON.
3. For e-waybill, vehicle details appended; failure responses logged with retries via Cloud Tasks exponential backoff.
4. Tenant admin UI displays status board fed by `gst_documents`.

## Payment Reconciliation
1. Nightly job downloads PG settlement reports into Cloud Storage.
2. Parser service loads data into staging table, matches against `payments` by order ID and date.
3. Fees, net payouts, and bank statements compared; mismatches beyond tolerance create review tasks.
4. Reports available via `/reports/payments` and exported to CSV.
