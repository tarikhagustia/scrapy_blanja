# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import html
import re
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from blanja.items import TransactionItem, CategoryItem, ProductItem, ShopItem, ProductViewItem, \
    ShopTotalSales, ProductReviewItem
from blanja.models import ProductDB, ShopDB, db_connect, DetailProductDB, \
    CategoryDB, ShopSalesTotalDB


class BlanjaPipeline(object):
    def __init__(self):
        """BlanjaPipeline
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item, TransactionItem):
            return self.handle_transaction(item)

        if isinstance(item, ProductItem):
            return self.handle_product(item)

        if isinstance(item, ShopItem):
            return self.handle_shop(item)

        if isinstance(item, CategoryItem):
            return self.handle_category(item)

        if isinstance(item, ProductViewItem):
            return self.handle_product_view(item)

        if isinstance(item, ShopTotalSales):
            return self.handle_shop_total(item)

        if isinstance(item, ProductReviewItem):
            return self.handle_product_review(item)

    def handle_transaction(self, item):
        session = self.Session()

        detail = DetailProductDB()
        detail.product_id = item['product'].product_id
        detail.shop_id = item['product'].shop_id
        detail.produk_yang_terjual = item['item_sold']
        detail.transaksi_sukses = item['success']
        detail.transaksi_dibatalkan = item['reject']
        detail.dilihat = 0
        detail.count_review = 0
        detail.rating = 0
        detail.created = datetime.now()
        detail.updated = datetime.now()
        session.merge(detail)
        session.commit()

        session.close()
        return item

    def handle_category(self, item):
        session = self.Session()

        current_category = session.query(CategoryDB).filter(CategoryDB.id_core == item['id']).first()
        if current_category is None:
            category = CategoryDB()
            category.id_core = item['id']
            category.name = item['name']
            category.parent_id = item['parent_id']
            category.url = item['url']
            category.text = item['name']

            session.merge(category)
            session.commit()
            session.close()
        session.close()
        return item

    def handle_product(self, item):
        session = self.Session()
        # Insert Product
        q_product = session.query(ProductDB).filter(ProductDB.product_id == item['product_id']).first()
        if q_product is None:
            product = ProductDB()
            product.product_id = item['product_id']
            product.shop_id = item['shop_id']
            product.kategori = item['category_id']
            product.kategori_text = ''
            product.sub_kategori = item['sub_category_id']
            product.sub_kategori_text = ''
            product.sub_kategori_child = ''
            product.name = item['name']
            product.url = item['url']
            product.image_url = item['image_url']
            product.price = item['price']
            product.original_price = item['price']
            product.created = datetime.now()
            product.updated = datetime.now()
            session.add(product)
            session.commit()

        session.close()
        return item

    def handle_shop(self, item):
        session = self.Session()
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        # Insert Shop
        q_shop = session.query(ShopDB).filter(ShopDB.id == item['id']).first()
        if q_shop is None:
            shop = ShopDB()
            shop.id = item['id']
            shop.name = re.sub('[^A-Za-z0-9\s?\'"]+', '', html.unescape(emoji_pattern.sub(r'', item['name'])))
            shop.url = item['url']
            shop.location = item['location']
            shop.city = item['city']
            shop.created = datetime.now()
            shop.updated = datetime.now()
            session.add(shop)
            session.commit()

        session.close()
        return item

    def handle_product_view(self, item):
        session = self.Session()

        q_daily = session.query(DetailProductDB).filter(
            DetailProductDB.product_id == item['product'].product_id).first()
        if q_daily:
            if "rb" in item['view']:
                numbers = re.findall('\d+', item['view'])
                dilihat = float(".".join(numbers)) * 1000
            else:
                dilihat = float(item['view'])
            q_daily.dilihat = dilihat
            session.commit()

        session.close()
        return item

    def handle_shop_total(self, item):
        session = self.Session()
        sales = ShopSalesTotalDB()
        sales.shop_id = item['shop_id']
        sales.total_penjualan = item['item_sold']
        session.merge(sales)
        session.commit()
        session.close()
        return item

    def handle_product_review(self, item):
        session = self.Session()

        q_daily = session.query(DetailProductDB).filter(
            DetailProductDB.product_id == item['product'].product_id).first()
        if q_daily:
            q_daily.count_review = float(item['total_review'])
            q_daily.rating = float(item['score'])
            session.commit()

        session.close()
        return item
