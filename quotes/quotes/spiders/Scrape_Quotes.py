# -*- coding: utf-8 -*-
import scrapy


class ScrapeQuotesSpider(scrapy.Spider):
    name = 'Scrape_Quotes'
    allowed_domains = ['quotes.toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]
    def parse(self, response):
        csrf_token = response.xpath('..//input[@name = "csrf_token"]//@value').extract()
        data = {
            'csrf_token' : csrf_token,
            'username' : 'abc',
            'password' : 'abc'
        }
        scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)
    def parse_quotes(self, response):
        quotes = response.xpath('.//span[@class="text"]//text()').extract()
        author = response.xpath('.//small[@class = "author"]//text()').extract()
        author_url = response.xpath('..//a[contains(text(),"Goodreads")]//@href').extract()
        for a,b,c in zip(quotes,author,author_url):
            data={
                    "quotes" : a,
                    "author" : b,
                    "URL" : c
            }
            yield data
        

