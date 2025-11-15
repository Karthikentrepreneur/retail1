'use client';

import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export function ProductsPanel() {
  const { data } = useQuery({
    queryKey: ['admin-products'],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE}/products`, {
        headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' }
      });
      return response.data;
    }
  });

  return (
    <section>
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Products</h2>
          <p className="text-sm text-slate-500">Manage catalog, pricing, and variants.</p>
        </div>
        <button className="rounded bg-emerald-600 px-4 py-2 text-white">Add Product</button>
      </header>
      <div className="mt-6 overflow-hidden rounded-lg border">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2 text-left font-medium">Name</th>
              <th className="px-4 py-2 text-left font-medium">SKU</th>
              <th className="px-4 py-2 text-left font-medium">Tax Group</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {(data || []).map((product: any) => (
              <tr key={product.id}>
                <td className="px-4 py-2">{product.name}</td>
                <td className="px-4 py-2">{product.sku}</td>
                <td className="px-4 py-2">{product.tax_group}</td>
              </tr>
            ))}
            {!data?.length && (
              <tr>
                <td colSpan={3} className="px-4 py-6 text-center text-slate-500">
                  No products yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
