'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

const reports = [
  { id: 'sales.daily', label: 'Daily Sales Summary' },
  { id: 'inventory.low_stock', label: 'Low Stock Report' },
  { id: 'gst.summary', label: 'GST Tax Summary' }
];

export default function ReportsPage() {
  const [selectedReport, setSelectedReport] = useState(reports[0].id);
  const mutation = useMutation({
    mutationFn: async (reportKey: string) => {
      const response = await axios.post(
        `${API_BASE}/reports/run`,
        { report_key: reportKey, filters: {} },
        { headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' } }
      );
      return response.data;
    }
  });

  return (
    <section className="p-6">
      <h2 className="text-2xl font-semibold">Reports</h2>
      <p className="text-sm text-slate-500">Generate analytics for sales, inventory, payments, and compliance.</p>
      <div className="mt-4 flex gap-4">
        <select
          className="rounded border px-3 py-2"
          value={selectedReport}
          onChange={(event) => setSelectedReport(event.target.value)}
        >
          {reports.map((report) => (
            <option key={report.id} value={report.id}>
              {report.label}
            </option>
          ))}
        </select>
        <button
          className="rounded bg-emerald-600 px-4 py-2 text-white"
          onClick={() => mutation.mutate(selectedReport)}
          disabled={mutation.isLoading}
        >
          {mutation.isLoading ? 'Generating…' : 'Generate'}
        </button>
      </div>
      {mutation.data && (
        <pre className="mt-6 max-h-96 overflow-y-auto rounded bg-slate-900 p-4 text-sm text-emerald-100">
          {JSON.stringify(mutation.data, null, 2)}
        </pre>
      )}
    </section>
  );
}
