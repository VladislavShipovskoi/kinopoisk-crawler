# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from kinopoisk.items import KinopoiskItem


BASE_URL = 'https://www.kinopoisk.ru/top/navigator/m_act%5Byears%5D/1890:2017/m_act%5Brating%5D/1:/order/rating/page/{}/#results'
SENTIMENT_DICT = {
    'response good': 'good',
    'response': 'neutral',
    'response bad': 'bad',
}


class FilmsSpider(CrawlSpider):
    name = "kinopoisk"
    allowed_domains = ["kinopoisk.ru"]
    start_urls = [
        BASE_URL.format('1')
    ]
    page = 1

    def parse(self, response):
        all_url = response.xpath('//div[@class = "info"]/div[@class="name"]/a/@href').extract()
        if all_url:
            for url in all_url:
                yield scrapy.Request(response.urljoin(url),callback=self.parse_movies)

            self.page += 1
            yield scrapy.Request(BASE_URL.format(self.page), callback=self.parse)

    def parse_movies(self,response):
        reviews_url = response.xpath('//li[@class="all"]/a/@href').extract_first()
        if reviews_url:
            yield scrapy.Request(response.urljoin(reviews_url), callback=self.parse_reviews)

    def parse_reviews(self, response):
        reviews = response.xpath('//div[@class="reviewItem userReview"]//div[@class="response good"]')
        if reviews:
            for review in reviews:
                review_item = KinopoiskItem()
                review_item['sentiment'] = SENTIMENT_DICT[review.xpath('@class').extract_first()]
                review_item['text'] = ' '.join((x.strip() for x in review.xpath('table//text()').extract() if x.strip()))

                yield review_item

            next_page = response.xpath('//a[text()="»"]/@href').extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse_reviews)
