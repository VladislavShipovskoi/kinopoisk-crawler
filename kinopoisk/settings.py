# -*- coding: utf-8 -*-

BOT_NAME = 'kinopoisk'

SPIDER_MODULES = ['kinopoisk.spiders']
NEWSPIDER_MODULE = 'kinopoisk.spiders'


ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'kinopoisk.pipelines.FilmsPipeline': 300,
}