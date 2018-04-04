import scrapy


class KinopoiskItem(scrapy.Item):
    movie = scrapy.Field()
    text = scrapy.Field()
    sentiment = scrapy.Field()
    author_link = scrapy.Field()