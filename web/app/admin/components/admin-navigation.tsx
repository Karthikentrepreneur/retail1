'use client';

const items = [
  { id: 'products', label: 'Products' },
  { id: 'inventory', label: 'Inventory' },
  { id: 'users', label: 'Users' },
  { id: 'pricing', label: 'Price Lists' }
] as const;

type AdminNavProps = {
  active: string;
  onSelect: (id: 'products' | 'inventory') => void;
};

export function AdminNavigation({ active, onSelect }: AdminNavProps) {
  return (
    <nav className="w-60 border-r bg-white">
      <ul className="space-y-1 p-4">
        {items.map((item) => (
          <li key={item.id}>
            <button
              className={`w-full rounded px-3 py-2 text-left text-sm ${
                active === item.id ? 'bg-emerald-100 text-emerald-700' : 'hover:bg-slate-100'
              }`}
              onClick={() => item.id in { products: true, inventory: true } && onSelect(item.id as 'products' | 'inventory')}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
