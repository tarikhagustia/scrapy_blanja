# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from blanja.models import db_connect, CategoryTransactionDB, SubCategoryTransactionDB


class BlanjaCategoryDailySpider(scrapy.Spider):
    name = 'blanja_category_daily'
    allowed_domains = ['tokopedia.com']

    def start_requests(self):
        # Get all Products
        engine = db_connect()
        session_maker = sessionmaker(bind=engine)

        session = session_maker()

        # Parent Category
        # Check daily_transaction
        sql = text('''
        SELECT
            SUM( c.produk_yang_terjual ) AS produk_yang_terjual,
            SUM( c.transaksi_sukses ) AS transaksi_sukses,
            SUM( c.transaksi_dibatalkan ) AS transaksi_dibatalkan,
            SUM( c.count_review ) AS count_review,
            SUM( c.dilihat ) AS dilihat,
            AVG( c.rating ) AS rating,
            ( SELECT MIN( price ) FROM products WHERE kategori = id_core ) AS min_price,
            ( SELECT MAX( price ) FROM products WHERE kategori = id_core ) AS max_price,
            ( SELECT COUNT( id ) FROM products WHERE kategori = id_core ) AS count_products,
            (SELECT COUNT(*) FROM (SELECT count(shop_id), kategori FROM shops JOIN products ON shops.id = products.shop_id GROUP BY shop_id, kategori) as tab WHERE tab.kategori = id_core) AS count_shop,
            x.id AS category_id 
        FROM
            kategori AS x
            JOIN products b ON b.kategori = id_core
            JOIN product_transactions_harian c ON c.product_id = b.product_id 
        WHERE
            parent_id = 0 
            AND c.date = DATE( NOW( ) ) 
        GROUP BY
            x.id_core
        ''')

        for result in session.execute(sql):
            produk_yang_terjual = result[0]
            transaksi_sukses = result[1]
            transaksi_dibatalkan = result[2]
            count_review = result[3]
            dilihat = result[4]
            rating = result[5]
            min_price = result[6]
            max_price = result[7]
            count_product = result[8]
            count_shop = result[9]
            id_core = result[10]

            # Insert if not exist
            trx = session.query(CategoryTransactionDB).filter(CategoryTransactionDB.kategori_id == id_core).filter(
                CategoryTransactionDB.date == datetime.now().date()).first()
            if trx:
                trx.produk_yang_terjual = produk_yang_terjual
                trx.transaksi_sukses = transaksi_sukses
                trx.transaksi_dibatalkan = transaksi_dibatalkan
                trx.count_review = count_review
                trx.dilihat = dilihat
                trx.rating = rating
                trx.min_harga = min_price
                trx.max_harga = max_price
                trx.jml_produk = count_product
                trx.jml_toko = count_shop
                session.commit()
            else:
                trx = CategoryTransactionDB()
                trx.kategori_id = id_core
                trx.produk_yang_terjual = produk_yang_terjual
                trx.transaksi_sukses = transaksi_sukses
                trx.transaksi_dibatalkan = transaksi_dibatalkan
                trx.count_review = count_review
                trx.dilihat = dilihat
                trx.rating = rating
                trx.min_harga = min_price
                trx.max_harga = max_price
                trx.jml_produk = count_product
                trx.jml_toko = count_shop
                session.add(trx)
                session.commit()

        sql = text('''
                SELECT
                    SUM( c.produk_yang_terjual ) AS produk_yang_terjual,
                    SUM( c.transaksi_sukses ) AS transaksi_sukses,
                    SUM( c.transaksi_dibatalkan ) AS transaksi_dibatalkan,
                    SUM( c.count_review ) AS count_review,
                    SUM( c.dilihat ) AS dilihat,
                    AVG( c.rating ) AS rating,
                    ( SELECT MIN( price ) FROM products WHERE sub_kategori = id_core ) AS min_price,
                    ( SELECT MAX( price ) FROM products WHERE sub_kategori = id_core ) AS max_price,
                    ( SELECT COUNT( id ) FROM products WHERE sub_kategori = id_core ) AS count_products,
                    (SELECT COUNT(*) FROM (SELECT count(shop_id), sub_kategori FROM shops JOIN products ON shops.id = products.shop_id GROUP BY shop_id, sub_kategori) as tab WHERE tab.sub_kategori = id_core) AS count_shop,
                    a.id AS category_id
                FROM
                    kategori AS a
                    JOIN products AS b ON b.sub_kategori = a.id_core
                    JOIN product_transactions_harian AS c ON c.product_id = b.product_id 
                WHERE
                    a.parent_id != 0 
                    AND c.date = DATE( NOW( ) )
                GROUP BY
                a.id_core
                ''')

        for result in session.execute(sql):
            produk_yang_terjual = result[0]
            transaksi_sukses = result[1]
            transaksi_dibatalkan = result[2]
            count_review = result[3]
            dilihat = result[4]
            rating = result[5]
            min_price = result[6]
            max_price = result[7]
            count_product = result[8]
            count_shop = result[9]
            id_core = result[10]

            # Insert if not exist
            trx = session.query(SubCategoryTransactionDB).filter(
                SubCategoryTransactionDB.kategori_id == id_core).filter(
                SubCategoryTransactionDB.date == datetime.now().date()).first()
            if trx:
                trx.produk_yang_terjual = produk_yang_terjual
                trx.transaksi_sukses = transaksi_sukses
                trx.transaksi_dibatalkan = transaksi_dibatalkan
                trx.count_review = count_review
                trx.dilihat = dilihat
                trx.rating = rating
                trx.min_harga = min_price
                trx.max_harga = max_price
                trx.jml_produk = count_product
                trx.jml_toko = count_shop
                session.commit()
            else:
                trx = SubCategoryTransactionDB()
                trx.kategori_id = id_core
                trx.produk_yang_terjual = produk_yang_terjual
                trx.transaksi_sukses = transaksi_sukses
                trx.transaksi_dibatalkan = transaksi_dibatalkan
                trx.count_review = count_review
                trx.dilihat = dilihat
                trx.rating = rating
                trx.min_harga = min_price
                trx.max_harga = max_price
                trx.jml_produk = count_product
                trx.jml_toko = count_shop
                session.add(trx)
                session.commit()
        yield scrapy.Request(url="https://blanja.com", callback=self.parse)

    def parse(self, response):
        pass
