# -*- coding: utf-8 -*-
import random
import sys
import time
import re
import redis
import scrapy
from scrapy import Request, Selector

from DoubanSpider.items import DoubanMovieItem

conn = redis.Redis(host="localhost", port=6379, db=0)
reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # movie_url = ['https://movie.douban.com/subject/25949777/',
    #              'https://movie.douban.com/subject/27107131/']
    movie_url = ['https://movie.Douban.com/subject/24773958/',
                 'https://movie.douban.com/subject/1292052/',
                 'https://movie.douban.com/subject/26969244/',
                 'https://movie.douban.com/subject/3604148/',
                 'https://movie.douban.com/subject/27133303/',
                 'https://movie.douban.com/subject/26363254/',
                 'https://movie.douban.com/subject/11584016/',
                 'https://movie.douban.com/subject/26972275/',
                 'https://movie.douban.com/subject/27107131/',
                 'https://movie.douban.com/subject/25949777/'
                 ]

    def start_requests(self):
        for url in self.movie_url:
            yield Request(url, self.parse_num)

    def parse_num(self, response):
        # print(response.headers)
        sel = Selector(response)
        follow_urls = sel.xpath('//div[@class="recommendations-bd"]/dl/dt/a/@href').extract()
        try:
            score = sel.xpath('//div[@class="rating_self clearfix"]/strong/text()').extract()[0]
        except:
            score = "暂无评分"
        sites = sel.xpath('//div[@id="info"]').extract()[0]
        title = sel.xpath('//div[@id="content"]/h1/span[1]//text()').extract()[0]
        if score == "暂无评分":
            number = "0"
        else:
            number = sel.xpath('//div[@id="interest_sectl"]//div[@class="rating_sum"]//text()').extract()[1]
        try:
            text = sel.xpath('//div[@id="link-report"]//text()[1]').extract()[1]
            if text.strip() == "":
                text = sel.xpath('//div[@id="link-report"]//text()[1]').extract()[2]
        except:
            text = ""
        # print(text.strip())
        # print(number)
        while '<' in sites:
            sites = sites.replace(sites[sites.index('<'):sites.index('>') + 1], "")
        site = sites.replace(" ", "")
        # print(title.split())
        item = DoubanMovieItem()
        item['length'] = "无"
        item['text'] = text.strip()
        item['number'] = number
        item['movie'] = title.strip()
        item['country'] = ""
        item['performer'] = ""
        item['type'] = ""
        item['show'] = ""
        item['length'] = ""
        item['director'] = ""
        item['performer'] = ""
        item['language'] = ""
        item['score'] = str(score)
        item['show2'] = ''
        item['jishu'] = ""
        item['jichang'] = ""
        for list in site.split('\n'):
            map = list.split(':')
            if map[0] == '集数':
                item['jishu'] = map[1]
            if map[0] == '单集片长':
                item['jichang'] = map[1]
                # print(item['jichang'])
            if map[0] == '导演':
                item['director'] = map[1]
            if map[0] == '主演':
                item['performer'] = map[1]
            if map[0] == '类型':
                item['type'] = map[1]
            if map[0] == '制片国家/地区':
                item['country'] = map[1]
            if map[0] == '语言':
                item['language'] = map[1]
            if map[0] == '上映日期':
                item['show'] = map[1]
            if map[0] == '首播':
                item['show2'] = map[1]
            if map[0] == '片长':
                item['length'] = map[1]
        # print(item)
        yield item

        for follow_url in follow_urls:
            flag = conn.sadd("Douban:movie", follow_url)
            if flag == 1:
                print(follow_url)
                yield Request(url=follow_url, callback=self.parse_num)


if __name__ == '__main__':
    import random

    # 生成随机数，浮点类型
    # 控制随机数的精度round(数值，精度)
    print round(random.uniform(1, 3), 2)
