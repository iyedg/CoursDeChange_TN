# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapybankscurrencyItem(scrapy.Item):
    date = scrapy.Field()
    bank = scrapy.Field()
    currency_code = scrapy.Field()
    buy_price = scrapy.Field()
    sell_price = scrapy.Field()
    unit = scrapy.Field()
