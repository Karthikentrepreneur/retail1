'use client';

import { usePOSStore } from '@/lib/stores/pos-store';

export function CartSummary() {
  const { cart, totals, removeFromCart, checkout } = usePOSStore();

  return (
    <section className="flex h-full flex-col rounded-lg border bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold">Cart</h2>
      <div className="mt-3 flex-1 space-y-2 overflow-y-auto">
        {cart.map((line) => (
          <div key={line.id} className="flex items-center justify-between rounded border px-3 py-2">
            <div>
              <p className="font-medium">{line.name}</p>
              <p className="text-sm text-slate-500">
                {line.quantity} × ₹{line.price.toFixed(2)}
              </p>
            </div>
            <button
              className="text-sm text-red-500 hover:underline"
              onClick={() => removeFromCart(line.id)}
            >
              Remove
            </button>
          </div>
        ))}
        {!cart.length && <p className="text-sm text-slate-500">Cart is empty</p>}
      </div>
      <div className="mt-4 border-t pt-4">
        <div className="flex justify-between text-sm">
          <span>Subtotal</span>
          <span>₹{totals.subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span>Tax</span>
          <span>₹{totals.tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-base font-semibold">
          <span>Total</span>
          <span>₹{totals.total.toFixed(2)}</span>
        </div>
        <button
          className="mt-4 w-full rounded bg-emerald-600 py-2 text-white transition hover:bg-emerald-700"
          onClick={() => checkout('cash')}
        >
          Collect Cash
        </button>
      </div>
    </section>
  );
}
