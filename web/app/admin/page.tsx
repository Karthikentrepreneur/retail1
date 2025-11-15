'use client';

import { useState } from 'react';
import { AdminNavigation } from './components/admin-navigation';
import { ProductsPanel } from './components/products-panel';
import { InventoryPanel } from './components/inventory-panel';

export default function AdminPage() {
  const [tab, setTab] = useState<'products' | 'inventory'>('products');

  return (
    <div className="flex h-full">
      <AdminNavigation active={tab} onSelect={setTab} />
      <main className="flex-1 overflow-y-auto p-6">
        {tab === 'products' && <ProductsPanel />}
        {tab === 'inventory' && <InventoryPanel />}
      </main>
    </div>
  );
}
