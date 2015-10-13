# -*- coding: utf-8 -*-
import scrapy
import unicodedata
from ondetrabalhar_scraper.items import OndetrabalharScraperItem
from scrapy import log


def normalize_text(text):
    return \
        unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')


class OndetrabalharSpider(scrapy.Spider):

    name = "ondetrabalhar"
    allowed_domains = ["ondetrabalhar.com"]
    start_urls = ["http://ondetrabalhar.com"]
    latest_entry = None
    first_entry = None

    def parse(self, response):
        # cmd line argument parsing
        if not self.first_entry:
            self.first_entry = int(self.start_entry) or 1
        # this grabs the latest entry to crawl - the first is provided via cmd
        # line or something else
        if not self.latest_entry:
            self.latest_entry = int(
                response.xpath("//ul[contains(@class,'jobs')]/a/@href")[0].extract().split('/')[-1])
            log.msg("First, Latest entry: (%s, %s)" %
                    (self.first_entry, self.latest_entry), level=log.DEBUG)
            self.start_urls = ["http://www.ondetrabalhar.com/vagas/%s" %
                               i for i in range(self.latest_entry, self.first_entry, -1)]
            log.msg("Start urls are: %s" %
                    (self.start_urls), level=log.DEBUG)
            for start_url in self.start_urls:
                yield scrapy.Request(url=start_url)
        else:
            job_title = normalize_text(response.xpath(
                "//*[contains(@class,'job-title')]//text()").extract()[0])
            job_location = normalize_text(response.xpath(
                "//*[contains(@class,'job-location')]//text()").extract()[0])
            job_meta = normalize_text(response.xpath(
                "//*[contains(@class,'job-meta')]//text()").extract()[0])
            howtoapply = normalize_text(''.join(response.xpath(
                "//*[contains(@class,'job-apply')]//text()").extract()))
            item = OndetrabalharScraperItem()
            item['title'] = job_title
            item['location'] = job_location
            item['meta'] = job_meta
            item['url'] = response.url
            item['howtoapply'] = howtoapply
            yield item
