import React from 'react';
import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useSale } from '../hooks/useSale';

export function SaleScreen() {
  const { products, query, setQuery, results, addLine, cartLines, totals, submitSale } = useSale();

  return (
    <View style={styles.container}>
      <View style={styles.searchSection}>
        <TextInput
          style={styles.input}
          placeholder="Scan barcode or search"
          value={query}
          onChangeText={setQuery}
        />
        <FlatList
          data={results}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <TouchableOpacity style={styles.result} onPress={() => addLine(item)}>
              <Text style={styles.resultName}>{item.name}</Text>
              <Text style={styles.resultPrice}>₹{item.price.toFixed(2)}</Text>
            </TouchableOpacity>
          )}
        />
      </View>
      <View style={styles.cartSection}>
        <Text style={styles.sectionTitle}>Cart</Text>
        <FlatList
          data={cartLines}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={styles.line}>
              <Text style={styles.lineName}>{item.name}</Text>
              <Text style={styles.lineQty}>{item.quantity} × ₹{item.price.toFixed(2)}</Text>
            </View>
          )}
        />
        <View style={styles.totals}>
          <Text>Subtotal: ₹{totals.subtotal.toFixed(2)}</Text>
          <Text>Tax: ₹{totals.tax.toFixed(2)}</Text>
          <Text style={styles.total}>Total: ₹{totals.total.toFixed(2)}</Text>
        </View>
        <TouchableOpacity style={styles.checkout} onPress={() => submitSale('cash')}>
          <Text style={styles.checkoutText}>Collect Cash</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, flexDirection: 'row', backgroundColor: '#fff' },
  searchSection: { flex: 1, padding: 16, borderRightWidth: 1, borderColor: '#e5e7eb' },
  cartSection: { flex: 1, padding: 16 },
  input: { borderWidth: 1, borderColor: '#d1d5db', borderRadius: 8, padding: 12, marginBottom: 12 },
  result: { padding: 12, borderWidth: 1, borderColor: '#d1d5db', borderRadius: 8, marginBottom: 8 },
  resultName: { fontSize: 16, fontWeight: '600' },
  resultPrice: { color: '#4b5563' },
  sectionTitle: { fontSize: 20, fontWeight: '700', marginBottom: 8 },
  line: { paddingVertical: 8, borderBottomWidth: 1, borderColor: '#e5e7eb' },
  lineName: { fontSize: 16 },
  lineQty: { color: '#6b7280' },
  totals: { marginTop: 16, gap: 4 },
  total: { fontSize: 18, fontWeight: '700' },
  checkout: { marginTop: 16, backgroundColor: '#047857', padding: 16, borderRadius: 8, alignItems: 'center' },
  checkoutText: { color: '#fff', fontWeight: '600' }
});
