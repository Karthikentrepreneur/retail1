'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

export default function TenantAdminPage() {
  const [flagKey, setFlagKey] = useState('gst_suite');
  const [enabled, setEnabled] = useState(true);
  const mutation = useMutation({
    mutationFn: async () => {
      await axios.put(
        `${API_BASE}/tenants/${localStorage.getItem('tenantId')}/feature-flags`,
        { flag_key: flagKey, enabled, rollout: {} },
        { headers: { 'X-Tenant-ID': localStorage.getItem('tenantId') || '' } }
      );
    }
  });

  return (
    <section className="max-w-2xl p-6">
      <h2 className="text-2xl font-semibold">Tenant Administration</h2>
      <p className="text-sm text-slate-500">Manage feature flags, plan add-ons, and compliance credentials.</p>
      <div className="mt-6 space-y-4">
        <div className="rounded border bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold">Feature Flags</h3>
          <div className="mt-4 flex items-center gap-4">
            <input
              className="flex-1 rounded border px-3 py-2"
              value={flagKey}
              onChange={(event) => setFlagKey(event.target.value)}
              placeholder="Flag key"
            />
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={enabled} onChange={(event) => setEnabled(event.target.checked)} /> Enabled
            </label>
            <button
              className="rounded bg-emerald-600 px-4 py-2 text-white"
              onClick={() => mutation.mutate()}
            >
              Save
            </button>
          </div>
          {mutation.isSuccess && <p className="mt-2 text-sm text-emerald-600">Flag updated successfully.</p>}
        </div>
      </div>
    </section>
  );
}
