# -*- coding: utf-8 -*-
import scrapy


class LaptopSpider(scrapy.Spider):
    name = 'Laptop'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/s?k=dell+laptop&lo=list&crid=3MUYSYE03280W&qid=1558948729&sprefix=dell+la%2Caps%2C463&ref=sr_pg_1']

    def parse(self, response):
        Next_URLs = response.xpath('..//a[text()="Next"]//@href').extract()
        for URL in Next_URLs:
            Actual_URL = 'https://www.amazon.com/'+URL
            yield scrapy.Request(Actual_URL,callback=self.parse_lap)
    def parse_lap(self, response):
        name = response.xpath('..//span[@class = "a-size-medium a-color-base a-text-normal"]//text()').extract()
        temp = response.xpath('..//span[@class = "a-price-whole"]//text()').extract()
        price = []
        for x in range(0,len(temp),2):
            price.append(temp[x])
        for a,b in zip(name,price):
            data = {
                "Model-Name" : a,
                "Price" : b
            }
            yield data
    
    def parse_detail(self, response):
        title = response.xpath('..//th[@class="a-color-secondary a-size-base prodDetSectionEntry"]//text()').extract()
        desc = response.xpath('..//td[@class="a-size-base"]//text()').extract()

        for a,b in zip(title, desc):
            data = {
                "Heading" : a,
                "Description" : b
            }
            yield data