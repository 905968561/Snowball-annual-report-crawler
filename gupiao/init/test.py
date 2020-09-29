import json
import time
import pymysql as py
import requests

url = "https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=SZ300757&type=Q4&is_detail=true&count=5&timestamp="
url1 = "https://xueqiu.com/S/SH601216"
url2 = 'https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SH601216'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=bv1214rr59; _ga=GA1.2.879653047.1594387410; xq_a_token=4072d5490c8abac330ccb4bf35d39715a0b208c5; xqat=4072d5490c8abac330ccb4bf35d39715a0b208c5; xq_r_token=cfa3a4ecd00a5ff784710d4faebc560f425b93fe; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk3Nzg3NTYwMzQsImlzcyI6InVjIiwiZXhwIjoxNTk4NTk5NTczLCJjdG0iOjE1OTYwMDc1NzMxOTMsImNpZCI6ImQ5ZDBuNEFadXAifQ.igTa0eJJx05rK9dUZfPZN0amIz2MPnrP15M6fzHv-hBwOaVeuWirf0KZql52Zfi-8sv2R2gD9d5zUayJKBfEPtfgbL1OTJvGFJcJpY4uhJ4hArBD10LquH0G1Vmbwz8MO0n2XGmVxl4ZT0HY-KdH9B2PvIc3_tMMz9sov1tlC98PZVwCbJ1wKbIve6epCvHla04mhDTVhdFwDcI0SSni00KbswMio4yN4UFi_-qH3sRsEsRJsF5s3dDztfXh54JBHkpYp79WzfpSP_N76vfhieFI-KEaN-n2sfc9o6r81y9QaUpjf8JFyQW0tgKaFOrXdS_x-aKv7e2q-MDSllCtCw; xq_is_login=1; u=9778756034; bid=3aa53dcb75c47a3f28f2f8510c436167_kd725iro; Hm_lvt_1db88642e346389874251b5a1eded6e3=1596008294,1596008380,1596008969,1596761710; snbim_minify=true; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1596763938',
    'Host': 'stock.xueqiu.com',
    'Origin': 'https://xueqiu.com',
    'Referer': 'https://xueqiu.com/snowman/S/SH600988/detail',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': '"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"',
}
headers1 = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=bv1214rr59; _ga=GA1.2.879653047.1594387410; __utmz=1.1594387413.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=4072d5490c8abac330ccb4bf35d39715a0b208c5; xqat=4072d5490c8abac330ccb4bf35d39715a0b208c5; xq_r_token=cfa3a4ecd00a5ff784710d4faebc560f425b93fe; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk3Nzg3NTYwMzQsImlzcyI6InVjIiwiZXhwIjoxNTk4NTk5NTczLCJjdG0iOjE1OTYwMDc1NzMxOTMsImNpZCI6ImQ5ZDBuNEFadXAifQ.igTa0eJJx05rK9dUZfPZN0amIz2MPnrP15M6fzHv-hBwOaVeuWirf0KZql52Zfi-8sv2R2gD9d5zUayJKBfEPtfgbL1OTJvGFJcJpY4uhJ4hArBD10LquH0G1Vmbwz8MO0n2XGmVxl4ZT0HY-KdH9B2PvIc3_tMMz9sov1tlC98PZVwCbJ1wKbIve6epCvHla04mhDTVhdFwDcI0SSni00KbswMio4yN4UFi_-qH3sRsEsRJsF5s3dDztfXh54JBHkpYp79WzfpSP_N76vfhieFI-KEaN-n2sfc9o6r81y9QaUpjf8JFyQW0tgKaFOrXdS_x-aKv7e2q-MDSllCtCw; xq_is_login=1; u=9778756034; bid=3aa53dcb75c47a3f28f2f8510c436167_kd725iro; __utma=1.879653047.1594387410.1596008333.1596761724.4; aliyungf_tc=AQAAAKFm8GbHyAgAkthcqxC6vnci56o4; acw_tc=2760825415969399806533988e83b9b22e32b44647c92b3261f0f706db1150; Hm_lvt_1db88642e346389874251b5a1eded6e3=1596008969,1596761710,1596852463,1596939981; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1596940307',
    'elastic-apm-traceparent': '00-270a684b6221c95c95b816b1b730e1c3-68cc4dfcb2e09aed-00',
    'Host': 'xueqiu.com',
    'Referer': 'https://xueqiu.com/S/SH601216',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
headers2 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=bv1214rr59; _ga=GA1.2.879653047.1594387410; xq_a_token=4072d5490c8abac330ccb4bf35d39715a0b208c5; xqat=4072d5490c8abac330ccb4bf35d39715a0b208c5; xq_r_token=cfa3a4ecd00a5ff784710d4faebc560f425b93fe; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk3Nzg3NTYwMzQsImlzcyI6InVjIiwiZXhwIjoxNTk4NTk5NTczLCJjdG0iOjE1OTYwMDc1NzMxOTMsImNpZCI6ImQ5ZDBuNEFadXAifQ.igTa0eJJx05rK9dUZfPZN0amIz2MPnrP15M6fzHv-hBwOaVeuWirf0KZql52Zfi-8sv2R2gD9d5zUayJKBfEPtfgbL1OTJvGFJcJpY4uhJ4hArBD10LquH0G1Vmbwz8MO0n2XGmVxl4ZT0HY-KdH9B2PvIc3_tMMz9sov1tlC98PZVwCbJ1wKbIve6epCvHla04mhDTVhdFwDcI0SSni00KbswMio4yN4UFi_-qH3sRsEsRJsF5s3dDztfXh54JBHkpYp79WzfpSP_N76vfhieFI-KEaN-n2sfc9o6r81y9QaUpjf8JFyQW0tgKaFOrXdS_x-aKv7e2q-MDSllCtCw; xq_is_login=1; u=9778756034; bid=3aa53dcb75c47a3f28f2f8510c436167_kd725iro; Hm_lvt_1db88642e346389874251b5a1eded6e3=1596008969,1596761710,1596852463,1596939981; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1596942009',
    'Host': 'stock.xueqiu.com',
    'Origin': 'https://xueqiu.com',
    'Referer': 'https://xueqiu.com/snowman/S/SH601216/detail',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}
r = requests.get(url=url, headers=headers2)
s = r.text
info = json.loads(s)
data = info['data']
print(s)
# l_date = data['listed_date']
# timeStamp = float(l_date/1000)
# timeArray = time.localtime(timeStamp)
# listed_date = time.strftime("%Y-%m-%d", timeArray)#上市日期
# print(listed_date)
# office_address_cn =data['office_address_cn']#公司所在地
# print(office_address_cn)
# c_name = data['org_name_cn']
# print(c_name)
# c_info = data['org_cn_introduction']
# print(c_info)
# c_tel = data['telephone']
# print(c_tel)
# import json
#
# import requests
#
# s = requests.get("https://api.bilibili.com/x/relation/followers?vmid=546195&pn=1&ps=100&order=desc&jsonp=jsonp")
# user = json.loads(s.text)
# data1 = user['data']['list'][0]['mid']
# data2 = user['ttl']
# print(data1)
