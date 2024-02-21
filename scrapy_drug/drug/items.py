# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    id_res = scrapy.Field()
    name = scrapy.Field()
    drug_no = scrapy.Field()
    effect = scrapy.Field()
    category = scrapy.Field()
    drug_base = scrapy.Field()
    source_link = scrapy.Field()
    type = scrapy.Field()
