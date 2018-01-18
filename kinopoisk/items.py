import scrapy


class KinopoiskItem(scrapy.Item):
    text = scrapy.Field()
    sentiment = scrapy.Field()