import { useEffect, useState } from 'react';
import axios from 'axios';
import { offlineStore } from '../storage/offlineStore';

const API_BASE = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://10.0.2.2:8000/api';

export function useSync() {
  const [pendingCount, setPendingCount] = useState(0);
  const [status, setStatus] = useState<'idle' | 'syncing' | 'error'>('idle');

  useEffect(() => {
    const interval = setInterval(() => {
      offlineStore.pendingSales().then((records) => setPendingCount(records.length));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const enqueueSync = (operation: any) => {
    // placeholder: would persist to sync table
  };

  const performSync = async () => {
    try {
      setStatus('syncing');
      const pending = await offlineStore.pendingSales();
      for (const sale of pending) {
        await axios.post(
          `${API_BASE}/sync/push`,
          {
            device_id: 'mobile-device',
            operations: [{ id: sale.id, type: 'sale', payload: JSON.parse(sale.payload) }]
          },
          { headers: { 'X-Tenant-ID': '' } }
        );
      }
      setStatus('idle');
    } catch (error) {
      setStatus('error');
    }
  };

  return { pendingCount, status, performSync, enqueueSync };
}
