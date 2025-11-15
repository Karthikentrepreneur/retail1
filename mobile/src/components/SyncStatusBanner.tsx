import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useSync } from '../sync/useSync';

export function SyncStatusBanner() {
  const { status, pendingCount, performSync } = useSync();

  if (status === 'idle' && pendingCount === 0) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.text}>
        {status === 'syncing' ? 'Syncing with server…' : `Pending sync: ${pendingCount}`}
      </Text>
      <TouchableOpacity style={styles.button} onPress={performSync}>
        <Text style={styles.buttonText}>Sync Now</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#f97316',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12
  },
  text: {
    color: '#fff',
    fontWeight: '600'
  },
  button: {
    backgroundColor: '#fff',
    borderRadius: 6,
    paddingHorizontal: 12,
    paddingVertical: 6
  },
  buttonText: {
    color: '#f97316',
    fontWeight: '600'
  }
});
