'use client';

import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { usePOSStore } from '@/lib/stores/pos-store';
import { ProductSearch } from './components/product-search';
import { CartSummary } from './components/cart-summary';

export default function POSPage() {
  const { loadProducts } = usePOSStore();
  const { data } = useQuery({
    queryKey: ['products'],
    queryFn: () => loadProducts()
  });

  useEffect(() => {
    if (data) {
      // preload cache for fast search
    }
  }, [data]);

  return (
    <div className="grid min-h-[calc(100vh-96px)] grid-cols-1 gap-4 p-6 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-4">
        <ProductSearch />
      </div>
      <div>
        <CartSummary />
      </div>
    </div>
  );
}
