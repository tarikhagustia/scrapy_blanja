# -*- coding: utf-8 -*-

import json

import scrapy
from sqlalchemy.orm import sessionmaker

from blanja.items import TransactionItem, ProductReviewItem
from blanja.models import db_connect, ProductDB


class BlanjaTransactionASpider(scrapy.Spider):
    name = 'blanja_transaction_a'
    allowed_domains = ['blanja.com']
    rotate_user_agent = True

    headers = {
        'Host': 'mapi.blanja.com',
        'blanja-timestamp': '1554190595545',
        'blanja-deviceid': '11440cdcfae490e54a8f8',
        'blanja-sign': '69c545c0175531fa56d94b46109b62de5a3bca5a'
    }

    def start_requests(self):
        engine = db_connect()
        session_maker = sessionmaker(bind=engine)

        session = session_maker()

        for product in session.query(ProductDB).all():
            id = product.product_id
            url = "https://mapi.blanja.com/api/v1/item/{}".format(id)
            yield scrapy.Request(url=url, callback=self.parse
                                 , headers=self.headers, meta={
                    'product': product
                });

    def parse(self, response):
        data = json.loads(response.body)

        review = data['ratingCount']
        sales = data['soldQuantity']
        rating = (data['rating'] / 20)

        item = TransactionItem()
        item['product'] = response.meta['product']
        item['item_sold'] = sales
        item['success'] = 0
        item['reject'] = 0
        yield item

        yield ProductReviewItem(product=response.meta['product'], score=rating, total_review=review)
