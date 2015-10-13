# -*- coding: utf-8 -*-
import scrapy
import unicodedata
from ondetrabalhar_scraper.items import OndetrabalharScraperItem


def normalize_text(text):
    return \
        unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
# str(text)
# text.encode('utf8')


class OndetrabalharSpider(scrapy.Spider):
    name = "ondetrabalhar"
    allowed_domains = ["ondetrabalhar.com"]
    start_urls = ["http://www.ondetrabalhar.com/vagas/%s" %
                  i for i in range(5686, 1, -1)]

    def parse(self, response):
        job_title = normalize_text(response.xpath(
            "//*[contains(@class,'job-title')]//text()").extract()[0])
        job_location = normalize_text(response.xpath(
            "//*[contains(@class,'job-location')]//text()").extract()[0])
        job_meta = normalize_text(response.xpath(
            "//*[contains(@class,'job-meta')]//text()").extract()[0])
        item = OndetrabalharScraperItem()
        item['title'] = job_title
        item['location'] = job_location
        item['meta'] = job_meta
        yield item
