import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'POS SaaS',
  description: 'Multi-tenant POS platform'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        <div className="min-h-screen flex flex-col">
          <header className="border-b bg-white px-6 py-4 shadow-sm">
            <h1 className="text-xl font-semibold">POS SaaS Console</h1>
          </header>
          <main className="flex-1">{children}</main>
        </div>
      </body>
    </html>
  );
}
