import { renderHook, act } from '@testing-library/react-hooks';

jest.mock('../src/storage/offlineStore', () => ({
  offlineStore: {
    getProducts: jest.fn().mockResolvedValue([]),
    saveSale: jest.fn().mockResolvedValue(undefined)
  }
}));

jest.mock('../src/sync/useSync', () => ({
  useSync: () => ({ enqueueSync: jest.fn(), pendingCount: 0, status: 'idle', performSync: jest.fn() })
}));

import { useSale } from '../src/hooks/useSale';

describe('useSale', () => {
  it('initializes totals to zero', async () => {
    const { result, waitForNextUpdate } = renderHook(() => useSale());
    await waitForNextUpdate();
    expect(result.current.totals.subtotal).toBe(0);
  });

  it('adds line items', () => {
    const { result } = renderHook(() => useSale());
    act(() => {
      result.current.addLine({ id: 'p1', name: 'Product', price: 10 });
    });
    expect(result.current.cartLines.length).toBe(1);
  });
});
