import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useSync } from '../sync/useSync';

export function HomeScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<any>>();
  const { pendingCount } = useSync();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>POS Mobile</Text>
      <Text style={styles.subtitle}>Offline-first Android billing</Text>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Sale')}>
        <Text style={styles.buttonText}>New Sale</Text>
      </TouchableOpacity>
      <Text style={styles.meta}>Pending sync: {pendingCount}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f5f5f5'
  },
  title: {
    fontSize: 28,
    fontWeight: '700'
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 24
  },
  button: {
    backgroundColor: '#047857',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8
  },
  buttonText: {
    color: '#fff',
    fontSize: 16
  },
  meta: {
    marginTop: 16,
    color: '#4b5563'
  }
});
