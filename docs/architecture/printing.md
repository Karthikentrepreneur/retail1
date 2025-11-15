# Printing Strategy

- **Templates**
  - 80mm thermal receipts rendered using ESC/POS templates stored in Cloud Storage. Backend exposes `/sales/{id}/print?format=escpos` returning base64 commands.
  - A4 invoices generated via server-side HTML → PDF (WeasyPrint) with GST-compliant layouts and optional pharmacy/doctor info.
  - Delivery challans share A4 template with toggled sections.
- **Triggering**
  - Web POS: prints via browser WebUSB/WebBluetooth integration calling local bridge that streams ESC/POS commands.
  - Android app: uses native module to send bytes over Bluetooth/USB to paired printer, with fallback to PDF view.
- **Cash Drawer**
  - ESC/POS command appended to thermal print job when payment mode includes cash.
- **Offline Support**
  - Android caches latest templates; includes version metadata to refresh after sync.
- **Security**
  - Signed URLs for PDF downloads; tokens expire in 5 minutes. Tenant ID embedded in template context.
