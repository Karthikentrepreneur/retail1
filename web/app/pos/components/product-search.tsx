'use client';

import { useState } from 'react';
import { usePOSStore } from '@/lib/stores/pos-store';

export function ProductSearch() {
  const [query, setQuery] = useState('');
  const { filteredProducts, addToCart } = usePOSStore();
  const products = filteredProducts(query);

  return (
    <section className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="flex items-center gap-2">
        <input
          className="w-full rounded border px-3 py-2"
          placeholder="Scan barcode or search by name"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>
      <div className="mt-4 grid max-h-96 grid-cols-1 gap-2 overflow-y-auto md:grid-cols-2">
        {products.map((product) => (
          <button
            key={product.id}
            className="rounded border px-3 py-2 text-left transition hover:border-slate-400"
            onClick={() => addToCart(product)}
          >
            <span className="font-medium">{product.name}</span>
            <span className="block text-sm text-slate-500">₹{product.price.toFixed(2)}</span>
          </button>
        ))}
        {!products.length && <p className="text-sm text-slate-500">No products found.</p>}
      </div>
    </section>
  );
}
