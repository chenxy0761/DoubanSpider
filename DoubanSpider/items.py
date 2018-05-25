# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie = scrapy.Field()
    type = scrapy.Field()
    length = scrapy.Field()
    performer = scrapy.Field()
    country = scrapy.Field()
    director = scrapy.Field()
    show = scrapy.Field()
    language = scrapy.Field()
    score = scrapy.Field()
    number = scrapy.Field()
    text = scrapy.Field()
    show2 = scrapy.Field()
    jishu = scrapy.Field()
    jichang = scrapy.Field()
