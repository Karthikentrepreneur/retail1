import { useEffect, useMemo, useState } from 'react';
import { useSync } from '../sync/useSync';
import { offlineStore } from '../storage/offlineStore';

type Product = {
  id: string;
  name: string;
  price: number;
};

type CartLine = Product & { id: string; quantity: number };

export function useSale() {
  const [products, setProducts] = useState<Product[]>([]);
  const [query, setQuery] = useState('');
  const [cartLines, setCartLines] = useState<CartLine[]>([]);
  const { enqueueSync } = useSync();

  useEffect(() => {
    offlineStore
      .getProducts()
      .then(setProducts)
      .catch(() => setProducts([]));
  }, []);

  const results = useMemo(() => {
    if (!query) return products;
    const normalized = query.toLowerCase();
    return products.filter((product) => product.name.toLowerCase().includes(normalized));
  }, [query, products]);

  const totals = useMemo(() => {
    const subtotal = cartLines.reduce((acc, line) => acc + line.price * line.quantity, 0);
    const tax = subtotal * 0.18;
    return { subtotal, tax, total: subtotal + tax };
  }, [cartLines]);

  const addLine = (product: Product) => {
    setCartLines((prev) => {
      const existing = prev.find((line) => line.id === product.id);
      if (existing) {
        return prev.map((line) => (line.id === product.id ? { ...line, quantity: line.quantity + 1 } : line));
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const submitSale = async (method: string) => {
    const payload = {
      invoice_temp_id: `MOB-${Date.now()}`,
      items: cartLines.map((line) => ({
        product_variant_id: line.id,
        quantity: line.quantity,
        unit_price: line.price,
        tax_group: 'standard'
      })),
      payments: [
        {
          method,
          amount: totals.total
        }
      ]
    };
    await offlineStore.saveSale(payload);
    enqueueSync({ type: 'sale', payload });
    setCartLines([]);
  };

  return { products, query, setQuery, results, addLine, cartLines, totals, submitSale };
}
