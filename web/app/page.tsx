import Link from 'next/link';

export default function HomePage() {
  return (
    <section className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-16">
      <h2 className="text-3xl font-bold">Welcome to POS SaaS</h2>
      <p className="text-slate-700">
        Select an area to continue working on sales, administration, tenant configuration, or reports.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        <Link href="/pos" className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md">
          <h3 className="text-xl font-semibold">POS</h3>
          <p>Start billing, manage holds, and collect payments.</p>
        </Link>
        <Link href="/admin" className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md">
          <h3 className="text-xl font-semibold">Admin Console</h3>
          <p>Manage products, users, and inventory operations.</p>
        </Link>
        <Link href="/tenant" className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md">
          <h3 className="text-xl font-semibold">Tenant Settings</h3>
          <p>Configure stores, taxes, feature flags, and billing plans.</p>
        </Link>
        <Link href="/reports" className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md">
          <h3 className="text-xl font-semibold">Reports</h3>
          <p>Review sales, inventory, payments, and GST analytics.</p>
        </Link>
      </div>
    </section>
  );
}
