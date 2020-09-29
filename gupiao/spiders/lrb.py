import json

from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider

from gupiao.items import Lrb_Info


class LRB(RedisCrawlSpider):
    name = 'info_lrb'
    redis_key = "job:lrb_link"

    def parse(self, response):
        cid = response.url[66:72]
        info = json.loads(response.text)
        data = info['data']
        name = data['quote_name']  # 公司名称
        for i in range(5):
            data_year = data['list'][i]
            year = data_year['report_name'][:4]
            try:
                cost_of_sales = data_year['sales_fee'][0]  # 销售成本
            except KeyError:
                cost_of_sales = 0
            if cost_of_sales == None:
                cost_of_sales = 0

            try:
                operating_costs = data_year['operating_costs'][0]  # 营业成本
            except KeyError:
                operating_costs = 0
            if operating_costs == None:
                operating_costs = 0

            try:
                operating_profits = data_year['op'][0]  # 营业利润
            except KeyError:
                operating_profits = 0
            if operating_profits == None:
                operating_profits = 0

            try:
                operating_income = data_year['total_revenue'][0]  # 营业收入
            except KeyError:
                operating_income = 0
            if operating_income == None:
                operating_income = 0

            try:
                netprofit = data_year['net_profit'][0]  # 净利润
            except KeyError:
                netprofit = 0
            if netprofit == None:
                netprofit = 0
            lrb_info = Lrb_Info()
            lrb_info['year'] = year
            lrb_info['cid'] = cid
            lrb_info['cost_of_sales'] = cost_of_sales
            lrb_info['operating_costs'] = operating_costs
            lrb_info['operating_profits'] = operating_profits
            lrb_info['operating_income'] = operating_income
            lrb_info['netprofit'] = netprofit
            yield lrb_info
