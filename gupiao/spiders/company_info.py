import json
import time

from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider

from gupiao.items import Company_Info


class LRB(RedisCrawlSpider):
    name = 'company_info'
    redis_key = "job:company_link"

    def parse(self, response):
        cid = response.url[-6:]  # 公司编号
        info = json.loads(response.text)
        data = info['data']['company']
        try:
            c_location = data['office_address_cn']  # 公司所在地
        except TypeError:
            c_location = ' '
        l_date = data['listed_date']
        timeStamp = float(l_date / 1000)
        timeArray = time.localtime(timeStamp)
        time_to_market = time.strftime("%Y-%m-%d", timeArray)  # 上市日期
        c_name = data['org_name_cn']  # 公司名称
        c_info = data['org_cn_introduction']  # 公司产业描述
        c_tel = data['telephone']  # 公司联系电话
        company_info = Company_Info()
        company_info['cid'] = cid
        company_info['c_location'] = c_location
        company_info['time_to_market'] = time_to_market
        company_info['c_name'] = c_name
        company_info['c_info'] = c_info
        company_info['c_tel'] = c_tel
        yield company_info
