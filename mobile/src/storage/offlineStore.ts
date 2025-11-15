import { Database, Q } from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';
import { mySchema } from './schema';
import { Sale, Product } from './models';

const adapter = new SQLiteAdapter({ schema: mySchema, dbName: 'pos.db' });
const database = new Database({ adapter, modelClasses: [Sale, Product] });

async function getProducts() {
  const collection = database.collections.get<Product>('products');
  const records = await collection.query().fetch();
  return records.map((record) => ({ id: record.id, name: record.name, price: record.price }));
}

async function saveSale(payload: any) {
  const collection = database.collections.get<Sale>('sales');
  await database.write(async () => {
    await collection.create((sale) => {
      sale.payload = JSON.stringify(payload);
      sale.status = 'pending';
    });
  });
}

async function pendingSales() {
  const collection = database.collections.get<Sale>('sales');
  return collection.query(Q.where('status', 'pending')).fetch();
}

export const offlineStore = { database, getProducts, saveSale, pendingSales };
