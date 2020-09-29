import scrapy


#深市公司代码
from gupiao.items import SZ_Link


class spider(scrapy.Spider):
    name = 'sz_link'
    # allowed_domains = ['mjtt.com']
    start_urls = ['https://www.banban.cn/gupiao/list_sz.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='u-postcontent cz']/ul/li")
        for li in li_list:
            linn = li.xpath("./a/text()").extract_first()
            c = filter(str.isdigit, linn)
            b = ''.join(c)
            link = SZ_Link()
            link['sz_code'] = b
            yield link