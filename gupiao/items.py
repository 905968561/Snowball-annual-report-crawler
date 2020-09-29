# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GupiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SH_Link(scrapy.Item):
    sh_code = scrapy.Field()


class SZ_Link(scrapy.Item):
    sz_code = scrapy.Field()


class CYB_Link(scrapy.Item):
    cyb_code = scrapy.Field()


class Lrb_Info(scrapy.Item):
    cid = scrapy.Field()
    year = scrapy.Field()
    cost_of_sales = scrapy.Field()
    operating_costs = scrapy.Field()
    operating_profits = scrapy.Field()
    operating_income = scrapy.Field()
    netprofit = scrapy.Field()


class Zcfzb_Info(scrapy.Item):
    year = scrapy.Field()
    cid = scrapy.Field()
    total_liab = scrapy.Field()
    inventory = scrapy.Field()
    account_receivable = scrapy.Field()
    shares = scrapy.Field()
    total_quity_atsopc = scrapy.Field()
    total_current_assets = scrapy.Field()
    total_assets = scrapy.Field()
    total_current_liab = scrapy.Field()


class Xjllb_Info(scrapy.Item):
    year = scrapy.Field()
    cid = scrapy.Field()
    ncf_from_oa = scrapy.Field()
    ncf_from_ia = scrapy.Field()
    ncf_from_fa = scrapy.Field()


class Company_Info(scrapy.Item):
    cid = scrapy.Field()
    c_location = scrapy.Field()
    time_to_market = scrapy.Field()
    c_name = scrapy.Field()
    c_info = scrapy.Field()
    c_tel = scrapy.Field()
# class Ttt(scrapy.Item):
#     xxx = scrapy.Field()
