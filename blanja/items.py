# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    parent_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class ProductItem(scrapy.Item):
    product_id = scrapy.Field()
    shop_id = scrapy.Field()
    category_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    shop_id = scrapy.Field()
    sub_category_id = scrapy.Field()


class TransactionItem(scrapy.Item):
    product = scrapy.Field()
    item_sold = scrapy.Field()
    success = scrapy.Field()
    reject = scrapy.Field()


class ShopItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    city = scrapy.Field()


class ProductViewItem(scrapy.Item):
    product = scrapy.Field()
    view = scrapy.Field()


class ShopTotalSales(scrapy.Item):
    shop_id = scrapy.Field()
    item_sold = scrapy.Field()


class ProductReviewItem(scrapy.Item):
    product = scrapy.Field()
    score = scrapy.Field()
    total_review = scrapy.Field()

class NoneItem(scrapy.Item):
    pass
