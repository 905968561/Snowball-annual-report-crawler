import scrapy


#创业板公司代码
from gupiao.items import CYB_Link


class spider(scrapy.Spider):
    name = 'cyb_link'
    # allowed_domains = ['mjtt.com']
    start_urls = ['https://www.banban.cn/gupiao/list_cyb.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='u-postcontent cz']/ul/li")
        for li in li_list:
            linn = li.xpath("./a/text()").extract_first()
            c = filter(str.isdigit, linn)
            b = ''.join(c)
            link = CYB_Link()
            link['cyb_code'] = b
            yield link