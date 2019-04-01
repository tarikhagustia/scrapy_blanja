# -*- coding: utf-8 -*-
import json

import scrapy

from blanja.items import CategoryItem


class BlanjaCategorySpider(scrapy.Spider):
    name = 'blanja_category'
    allowed_domains = ['blanja.com']
    rotate_user_agent = True
    category_url = "https://www.blanja.com/katalog/c"

    def start_requests(self):
        yield scrapy.Request(url="https://item.blanja.com/navigation/backendCategory?device=PC", callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        url = data['categoryUrl']
        for main_category in data['mappingLvlCategory']:
            for category in data['mappingLvlCategory'][main_category]:
                item_category = CategoryItem()
                item_category['id'] = category['id']
                item_category['parent_id'] = category['parentId']
                item_category['name'] = category['name']
                item_category['url'] = url + '/{}/{}'.format(category['menuDisplay'], category['urlKey'])
                yield item_category
                self.process_category(category)

    def process_category(self, parent):
        if len(parent['children']) > 0:
            for child in parent['children']:
                item_category = CategoryItem()
                item_category['id'] = child['id']
                item_category['parent_id'] = child['parentId']
                item_category['name'] = child['name']
                item_category['url'] = self.category_url + '/{}/{}'.format(child['menuDisplay'], child['urlKey'])
                yield item_category
                if len(parent['children']) > 0:
                    self.process_category(child)
