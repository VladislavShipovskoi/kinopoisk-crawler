# -*- coding: utf-8 -*-


class FilmsPipeline(object):
    def process_item(self, item, spider):
        return item