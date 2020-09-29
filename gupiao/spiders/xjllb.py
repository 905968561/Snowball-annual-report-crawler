import json

from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider

from gupiao.items import Xjllb_Info


class LRB(RedisCrawlSpider):
    name = 'info_xjllb'
    redis_key = "job:xjllb_link"

    def parse(self, response):
        cid = response.url[69:75]
        info = json.loads(response.text)
        data = info['data']
        name = data['quote_name']  # 公司名称
        for i in range(5):
            data_year = data['list'][i]
            year = data_year['report_name'][:4]
            try:
                ncf_from_oa = data_year['ncf_from_oa'][0]  # 经营活动产生的现金流量净额
            except KeyError:
                ncf_from_oa = 0
            if ncf_from_oa == None:
                ncf_from_oa = 0

            try:
                ncf_from_ia = data_year['ncf_from_ia'][0]  # 投资活动产生的现金流量净额
            except KeyError:
                ncf_from_ia = 0
            if ncf_from_ia == None:
                ncf_from_ia = 0

            try:
                ncf_from_fa = data_year['ncf_from_fa'][0]  # 筹资活动产生的现金流量净额
            except KeyError:
                ncf_from_fa = 0
            if ncf_from_fa == None:
                ncf_from_fa = 0
            xjllb_info = Xjllb_Info()
            xjllb_info['year'] = year
            xjllb_info['cid'] = cid
            xjllb_info['ncf_from_oa'] = ncf_from_oa
            xjllb_info['ncf_from_ia'] = ncf_from_ia
            xjllb_info['ncf_from_fa'] = ncf_from_fa
            yield xjllb_info
