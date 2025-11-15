'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/use-auth';

export function TopNav() {
  const { token, logout } = useAuth();

  return (
    <nav className="flex items-center justify-between bg-white px-6 py-3 shadow-sm">
      <div className="flex items-center gap-4">
        <span className="text-lg font-semibold">POS SaaS</span>
        <Link href="/pos" className="text-sm text-slate-600 hover:text-slate-900">
          POS
        </Link>
        <Link href="/admin" className="text-sm text-slate-600 hover:text-slate-900">
          Admin
        </Link>
        <Link href="/reports" className="text-sm text-slate-600 hover:text-slate-900">
          Reports
        </Link>
      </div>
      <div className="text-sm text-slate-500">
        {token ? (
          <button onClick={logout} className="rounded bg-slate-100 px-3 py-1 hover:bg-slate-200">
            Sign out
          </button>
        ) : (
          <Link href="/login" className="rounded bg-emerald-600 px-3 py-1 text-white">
            Sign in
          </Link>
        )}
      </div>
    </nav>
  );
}
