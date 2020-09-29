import json

from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider

from gupiao.items import Zcfzb_Info


class LRB(RedisCrawlSpider):
    name = 'info_zcfzb'
    redis_key = "job:zcfzb_link"

    def parse(self, response):
        cid = response.url[67:73]
        info = json.loads(response.text)
        data = info['data']
        name = data['quote_name']  # 公司名称
        for i in range(5):
            data_year = data['list'][i]
            year = data_year['report_name'][:4]
            try:
                total_liab = data_year['total_liab'][0]  # 负债合计
            except KeyError:
                total_liab = 0
            if total_liab == None:
                total_liab = 0

            try:
                inventory = data_year['inventory'][0]  # 存货总计
            except KeyError:
                inventory = 0
            if inventory == None:
                inventory = 0

            try:
                account_receivable = data_year['account_receivable'][0]  # 应收账款总计
            except KeyError:
                account_receivable = 0
            if account_receivable == None:
                account_receivable = 0

            try:
                shares = data_year['shares'][0]  # 实收资本总计
            except KeyError:
                shares = 0
            if shares == None:
                shares = 0

            try:
                total_quity_atsopc = data_year['total_liab_and_holders_equity'][0]  # 所有者权益总计
            except KeyError:
                total_quity_atsopc = 0
            if total_quity_atsopc == None:
                total_quity_atsopc = 0

            try:
                total_current_assets = data_year['total_current_assets'][0]  # 流动资产合计
            except KeyError:
                total_current_assets = 0
            if total_current_assets == None:
                total_current_assets = 0

            try:
                total_assets = data_year['total_assets'][0]  # 资产总计
            except KeyError:
                total_assets = 0
            if total_assets == None:
                total_assets = 0

            try:
                total_current_liab = data_year['total_current_liab'][0]  # 流动负债
            except KeyError:
                total_current_liab = 0
            if total_current_liab == None:
                total_current_liab = 0

            zcfzb_info = Zcfzb_Info()
            zcfzb_info['year'] = year
            zcfzb_info['cid'] = cid
            zcfzb_info['total_liab'] = total_liab
            zcfzb_info['inventory'] = inventory
            zcfzb_info['account_receivable'] = account_receivable
            zcfzb_info['shares'] = shares
            zcfzb_info['total_quity_atsopc'] = total_quity_atsopc
            zcfzb_info['total_current_assets'] = total_current_assets
            zcfzb_info['total_assets'] = total_assets
            zcfzb_info['total_current_liab'] = total_current_liab
            yield zcfzb_info
