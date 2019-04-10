# -*- coding: utf-8 -*-
import json

import scrapy
from sqlalchemy.orm import sessionmaker

from blanja.items import ProductItem, ShopItem
from blanja.models import db_connect, CategoryDB


class BlanjaProductDSpider(scrapy.Spider):
    name = 'blanja_product_d'
    allowed_domains = ['blanja.com']
    rotate_user_agent = True

    def start_requests(self):
        # Get all Products
        engine = db_connect()
        session_maker = sessionmaker(bind=engine)

        session = session_maker()
        # Makanan &amp; Minuman, Otomotif, Hobi, Buku &amp; Mainan
        for category in session.query(CategoryDB).filter(CategoryDB.parent_id.in_([20000010, 20000011, 20000012])):
            page_no = 1
            category_id = category.id_core
            yield scrapy.Request(
                url="https://item.blanja.com/items/a/search?oneNav={}&pageNo=1".format(category_id),
                callback=self.parse, meta={
                    "page_no": page_no,
                    "category": category_id,
                    "parent": category.parent_id
                })

    def parse(self, response):
        products = response.xpath('//div[@class="product-box"]')
        json_products = [] if response.css("#gtm-param").xpath('@value').extract_first() is None else json.loads(
            response.css("#gtm-param").xpath('@value').extract_first())
        category = response.meta['category']
        parent = response.meta['parent']
        current_page = response.meta['page_no']
        for product in products:
            shop_name = product.xpath(
                'div[@class="product-desc"]/div[@class="product-store clearfix"]/div/a/div/text()').extract_first()
            shop_id = product.css("img.lazy").xpath("@data-original").extract_first().split("/")[5]
            shop_url = product.css("a.shop-name").xpath("@href").extract_first()
            product_id = product.css('div.product-like').xpath('@itemid').extract_first()
            product_name = product.xpath('div[@class="product-desc"]/a/h3//text()').extract_first()
            product_url = product.css('a.prod-anchor').xpath('@href').extract_first()
            product_img = product.css("img.lazy").xpath("@data-original").extract_first()
            product_price = json_products[product_id]['price']
            yield ShopItem(id=shop_id, name=shop_name, url=shop_url, location="", city="")

            product = ProductItem()
            product['product_id'] = product_id
            product['name'] = product_name
            product['url'] = product_url
            product['image_url'] = product_img
            product['price'] = product_price
            product['shop_id'] = shop_id
            product['sub_category_id'] = category
            product['category_id'] = parent

            yield product

        # Check other products
        total_page = response.xpath('//span[@class="recnum"]/@data').extract_first()
        if int(total_page) > current_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url="https://item.blanja.com/items/a/search?oneNav={}&pageNo={}".format(category, next_page),
                callback=self.parse, meta={
                    "page_no": next_page,
                    "category": category,
                    "parent": parent,
                })
