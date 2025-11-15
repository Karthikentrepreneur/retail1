import { appSchema, tableSchema } from '@nozbe/watermelondb';

export const mySchema = appSchema({
  version: 1,
  tables: [
    tableSchema({
      name: 'products',
      columns: [
        { name: 'name', type: 'string' },
        { name: 'price', type: 'number' }
      ]
    }),
    tableSchema({
      name: 'sales',
      columns: [
        { name: 'payload', type: 'string' },
        { name: 'status', type: 'string' }
      ]
    })
  ]
});
