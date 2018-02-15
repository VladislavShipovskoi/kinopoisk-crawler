import scrapy


class KinopoiskItem(scrapy.Item):
    text = scrapy.Field()
    sentiment = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()