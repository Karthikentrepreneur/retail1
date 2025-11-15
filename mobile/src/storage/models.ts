import { Model } from '@nozbe/watermelondb';
import { field, text } from '@nozbe/watermelondb/decorators';

export class Product extends Model {
  static table = 'products';

  @text('name')
  declare name: string;

  @field('price')
  declare price: number;
}

export class Sale extends Model {
  static table = 'sales';

  @text('payload')
  declare payload: string;

  @text('status')
  declare status: string;
}
