'use client';

import { create } from 'zustand';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

type CartLine = {
  id: string;
  productId: string;
  name: string;
  price: number;
  quantity: number;
};

type POSState = {
  products: { id: string; name: string; price: number }[];
  cart: CartLine[];
  totals: { subtotal: number; tax: number; total: number };
  loadProducts: () => Promise<{ id: string; name: string; price: number }[]>;
  filteredProducts: (query: string) => { id: string; name: string; price: number }[];
  addToCart: (product: { id: string; name: string; price: number }) => void;
  removeFromCart: (id: string) => void;
  checkout: (method: string) => Promise<void>;
};

export const usePOSStore = create<POSState>((set, get) => ({
  products: [],
  cart: [],
  totals: { subtotal: 0, tax: 0, total: 0 },
  loadProducts: async () => {
    const response = await axios.get(`${API_BASE}/products`, {
      headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' }
    });
    const products = response.data.map((product: any) => ({
      id: product.id,
      name: product.name,
      price: product.price_sale || product.price || 0
    }));
    set({ products });
    return products;
  },
  filteredProducts: (query) => {
    const products = get().products;
    if (!query) return products;
    const normalized = query.toLowerCase();
    return products.filter((product) => product.name.toLowerCase().includes(normalized));
  },
  addToCart: (product) => {
    set((state) => {
      const existing = state.cart.find((line) => line.productId === product.id);
      let cart: CartLine[];
      if (existing) {
        cart = state.cart.map((line) =>
          line.productId === product.id ? { ...line, quantity: line.quantity + 1 } : line
        );
      } else {
        cart = [...state.cart, { id: crypto.randomUUID(), productId: product.id, name: product.name, price: product.price, quantity: 1 }];
      }
      const subtotal = cart.reduce((acc, line) => acc + line.price * line.quantity, 0);
      const tax = subtotal * 0.18;
      return { cart, totals: { subtotal, tax, total: subtotal + tax } };
    });
  },
  removeFromCart: (id) => {
    set((state) => {
      const cart = state.cart.filter((line) => line.id !== id);
      const subtotal = cart.reduce((acc, line) => acc + line.price * line.quantity, 0);
      const tax = subtotal * 0.18;
      return { cart, totals: { subtotal, tax, total: subtotal + tax } };
    });
  },
  checkout: async (method) => {
    const state = get();
    if (!state.cart.length) return;
    await axios.post(
      `${API_BASE}/sales`,
      {
        store_id: localStorage.getItem('storeId'),
        items: state.cart.map((line) => ({
          product_variant_id: line.productId,
          quantity: line.quantity,
          unit_price: line.price,
          tax_group: 'standard',
          discount_amount: 0
        })),
        payments: [
          {
            method,
            amount: state.totals.total
          }
        ]
      },
      { headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' } }
    );
    set({ cart: [], totals: { subtotal: 0, tax: 0, total: 0 } });
  }
}));
