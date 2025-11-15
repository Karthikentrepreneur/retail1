'use client';

import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export function InventoryPanel() {
  const { data } = useQuery({
    queryKey: ['admin-inventory'],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE}/inventory/stock`, {
        headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' }
      });
      return response.data;
    }
  });

  return (
    <section>
      <header>
        <h2 className="text-2xl font-semibold">Inventory</h2>
        <p className="text-sm text-slate-500">Track stock across warehouses and stores.</p>
      </header>
      <div className="mt-6 overflow-hidden rounded-lg border">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2 text-left font-medium">Warehouse</th>
              <th className="px-4 py-2 text-left font-medium">Product Variant</th>
              <th className="px-4 py-2 text-left font-medium">On Hand</th>
              <th className="px-4 py-2 text-left font-medium">Reserved</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {(data || []).map((row: any) => (
              <tr key={`${row.warehouse_id}-${row.product_variant_id}`}>
                <td className="px-4 py-2">{row.warehouse_id}</td>
                <td className="px-4 py-2">{row.product_variant_id}</td>
                <td className="px-4 py-2">{row.qty_on_hand}</td>
                <td className="px-4 py-2">{row.qty_reserved}</td>
              </tr>
            ))}
            {!data?.length && (
              <tr>
                <td colSpan={4} className="px-4 py-6 text-center text-slate-500">
                  Inventory balances not available.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
