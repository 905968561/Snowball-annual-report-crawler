# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
import pymysql as py

from gupiao.items import SH_Link, SZ_Link, CYB_Link, Lrb_Info, Company_Info, Zcfzb_Info, Xjllb_Info


# 亲测当短时间访问次数超过2000次时，雪球网大概率会进行登录验证，可以存入不同的redis job 来进行多次分批爬取
# https: // stock.xueqiu.com / v5 / stock / finance / cn / income.json?symbol = SZ300122 & type = Q4 & is_detail = true & count = 5 & timestamp =
# https: // stock.xueqiu.com / v5 / stock / finance / cn / income.json?symbol = SH601318 & type = Q4 & is_detail = true & count = 5 & timestamp =
# https: // stock.xueqiu.com / v5 / stock / finance / cn / balance.json?symbol = SZ300820 & type = Q4 & is_detail = true & count = 5 & timestamp =
# https: // stock.xueqiu.com / v5 / stock / finance / cn / cash_flow.json?symbol = SZ300820 & type = Q4 & is_detail = true & count = 5 & timestamp =

#将年报链接注入redis数据库
# 沪市
def push_lrb_sh(redis_conn, item):
    redis_conn.rpush("job:lrb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol=SH" + item[
        "sh_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_zcfzb_sh(redis_conn, item):
    redis_conn.rpush("job:zcfzb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?symbol=SH" + item[
        "sh_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_xjllb_sh(redis_conn, item):
    redis_conn.rpush("job:xjllb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=SH" + item[
        "sh_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_company_sh(redis_conn, item):
    redis_conn.rpush("job:company_link", "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SH" + item[
        "sh_code"])


# 深市
def push_lrb_sz(redis_conn, item):
    redis_conn.rpush("job:lrb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol=SZ" + item[
        "sz_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_zcfzb_sz(redis_conn, item):
    redis_conn.rpush("job:zcfzb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?symbol=SZ" + item[
        "sz_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_xjllb_sz(redis_conn, item):
    redis_conn.rpush("job:xjllb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=SZ" + item[
        "sz_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_company_sz(redis_conn, item):
    redis_conn.rpush("job:company_link", "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SZ" + item[
        "sz_code"])


# 创业板（深市）
def push_lrb_cyb(redis_conn, item):
    redis_conn.rpush("job:lrb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol=SZ" + item[
        "cyb_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_zcfzb_cyb(redis_conn, item):
    redis_conn.rpush("job:zcfzb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?symbol=SZ" + item[
        "cyb_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_xjllb_cyb(redis_conn, item):
    redis_conn.rpush("job:xjllb_link", "https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?symbol=SZ" + item[
        "cyb_code"] + "&type=Q4&is_detail=true&count=5&timestamp=")


def push_company_cyb(redis_conn, item):
    redis_conn.rpush("job:company_link", "https://stock.xueqiu.com/v5/stock/f10/cn/company.json?symbol=SZ" + item[
        "cyb_code"])


class GupiaoPipeline:
    def __init__(self):
        pool = redis.ConnectionPool(host="localhost", port=6379, max_connections=1024)
        # 创建连接对象
        conn = redis.Redis(connection_pool=pool)
        self.redis_conn = conn

    def process_item(self, item, spider):
        # link 初始化
        if isinstance(item, SH_Link):
            push_lrb_sh(self.redis_conn, item)
            push_zcfzb_sh(self.redis_conn, item)
            push_xjllb_sh(self.redis_conn, item)
            push_company_sh(self.redis_conn, item)
        elif isinstance(item, SZ_Link):
            push_lrb_sz(self.redis_conn, item)
            push_zcfzb_sz(self.redis_conn, item)
            push_xjllb_sz(self.redis_conn, item)
            push_company_sz(self.redis_conn, item)
        elif isinstance(item, CYB_Link):
            push_lrb_cyb(self.redis_conn, item)
            push_zcfzb_cyb(self.redis_conn, item)
            push_xjllb_cyb(self.redis_conn, item)
            push_company_cyb(self.redis_conn, item)
        elif isinstance(item, Lrb_Info):
            conn = py.connect("localhost", "root", "root", "gupiao")
            cursor = conn.cursor()
            # create_table = '''
            #                     '''
            # cursor.execute(create_table)
            insert = '''
                                insert into t_income_statement(i_year,cost_of_sales,operating_costs,operating_profits,operating_income,netprofit,
                                c_id
                                ) values
                                ('%s','%s','%s','%s','%s','%s','%s');
                                ''' % (
                item['year'], item['cost_of_sales'], item['operating_costs'], item['operating_profits'],
                item['operating_income'], item['netprofit'], item['cid'])
            cursor.execute(insert)
            conn.commit()
            cursor.close()
            conn.close()
        elif isinstance(item, Company_Info):
            conn = py.connect("localhost", "root", "root", "gupiao")
            cursor = conn.cursor()
            # create_table = '''
            #                     '''
            # cursor.execute(create_table)
            insert = '''
                                insert into t_company(c_id,c_location,time_to_market,c_name,c_industry,c_tel
                                ) values
                                ('%s','%s','%s','%s','%s','%s');
                                ''' % (
                item['cid'], item['c_location'], item['time_to_market'], item['c_name'],
                item['c_info'], item['c_tel'])
            cursor.execute(insert)
            conn.commit()
            cursor.close()
            conn.close()
        elif isinstance(item, Zcfzb_Info):
            conn = py.connect("localhost", "root", "root", "gupiao")
            cursor = conn.cursor()
            # create_table = '''
            #                     '''
            # cursor.execute(create_table)
            insert = '''
                                insert into t_balance_sheet(b_year,total_liabilities,average_inventory,average_accounts_receivable
                                ,average_paid_in_capital,average_owner_equity,total_current_liabikities,average_current_assets,average_total_assets
                                ,c_id
                                ) values
                                ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
                                ''' % (
                item['year'], item['total_liab'], item['inventory'], item['account_receivable'],
                item['shares'], item['total_quity_atsopc'], item['total_current_liab'], item['total_current_assets'],
                item['total_assets'], item['cid'])
            cursor.execute(insert)
            conn.commit()
            cursor.close()
            conn.close()
        elif isinstance(item, Xjllb_Info):
            conn = py.connect("localhost", "root", "root", "gupiao")
            cursor = conn.cursor()
            # create_table = '''
            #                     '''
            # cursor.execute(create_table)
            insert = '''
                                insert into t_cash_flow_statement(c_id,c_year,net_cash_flow_frow_from_operating_activities,
                                net_cash_flows_from_investing_activities,net_cash_flows_from_financing_activities
                                ) values
                                ('%s','%s','%s','%s','%s');
                                ''' % (
                item['cid'], item['year'], item['ncf_from_oa'], item['ncf_from_ia'],
                item['ncf_from_fa'])
            cursor.execute(insert)
            conn.commit()
            cursor.close()
            conn.close()
