# import xml element tree
import xml.etree.ElementTree as ET
import requests
# import mysql connector
import mysql.connector
from mysql import connector
import datetime
from datetime import date, timedelta
import time
from iiko_client import IikoClient
from iiko_auth import IikoServer

conn = connector.connect(user='root',
                         password='erlan1990',
                         host='localhost',
                         database='bahandireport',
                         auth_plugin='mysql_native_password')

""" TODO
[]Показатели для Daily Sales Report
[*]Количество заказов в день
[*]Касса в день
[*]Средний заказ
[]Закуп в день в тенге  (приход продукции, накладные) (цеха, точки, города)
[]Себестоимость в тенге
[]Расход в день в тенге (акты реализации, списание, перемещение)
[*]Заказ на сегодня в тенге
"""


IIKO_URL = 'https://bahandi-co.iiko.it'
IIKO_LOGIN = 'Keng1'
IIKO_PASSWORD = '37a7d5806f9d502b67bc96109eaa91918ac1d53b'

iiko_log = IikoServer(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD)
IIKO_VERSION = iiko_log.get_version()
IIKO_TOKEN = iiko_log.auth()


iiko_cleint = IikoClient(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD, IIKO_VERSION, IIKO_TOKEN)
todaydate = date.today() - timedelta(days=1)
nextdate = date.today()
str_date = todaydate.strftime("%Y-%m-%d")
strn_date = nextdate.strftime("%Y-%m-%d")
# aggr_sales = iiko_cleint.casshift_by_aggregators(str_date, strn_date)
# parse_aggr = ET.fromstring(aggr_sales)
# for et in parse_aggr.iter("i"):
#     if len(data := et.findall("v")) == 4:
#         table = """INSERT INTO test(date,department,cash_sum,paytype) VALUES(%s,%s,%s,%s)"""
#         date, department, cash_sum, paytype = (x.text for x in data)
#         print(date, department, cash_sum, paytype)
#         c = conn.cursor()
#         c.execute(table, (date, department, cash_sum, paytype))
#         conn.commit()


def get_oversales ():

    overall_sales = iiko_cleint.casshift_sum_report(str_date)
    parse_overs = ET.fromstring(overall_sales)
    data_overs = parse_overs.findall('date')

    # from xml.etree import ElementTree as ET
    # tree = ET.parse("doc.xml")
    # root = tree.getroot()
    # for et in root.iter("i"):
    #     if len(data := et.findall("v")) == 3:
    #         department, amount, service = (x.text for x in data)
    for i in data_overs:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('v/cls=java.lang.String')
        cash_sum = i.find('v/cls=java.math.BigDecimal')

    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()
# print('asdfasfsa')


def get_aggrsales ():
    print('asfsafdafa')
    aggr_sales = iiko_cleint.casshift_by_aggregators(str_date, strn_date)
    parse_aggr = ET.fromstring(aggr_sales)
    for et in parse_aggr.iter("i"):
        if len(data := et.findall("v")) == 4:
            table = """INSERT INTO test(date,department,cash_sum,paytype) VALUES(%s,%s,%s,%s)"""
            date, department, cash_sum, paytype = (x.text for x in data)
            print(date, department, cash_sum, paytype)
            c = conn.cursor()
            c.execute(table, (date, department, cash_sum, paytype))
            conn.commit()

# def get_pricecost ():
#
#     price_cost = iiko_cleint.cost_price(str_date, strn_date)
#     parse_pcost = ET.fromstring(price_cost)
#     data_pc = parse_pcost.findall('date')
#
#     for i in data_pc:
#         date = i.find('v/cls=java.util.Date типо такого')
#         store_id = i.find()
#         over_sales = i.find()
#         cost_price = i.find('v/cls=java.math.BigDecimal')
#     table = """INSERT INTO price_cost(date,store_id,over_sales,cost_price) VALUES(%s,%s,%s,%s,%s)"""
#
#     for i in table:
#         c = conn.cursor()
#         c.execute(table, date, store_id, over_sales, cost_price)
#         conn.commit()

# def get_storeitems():
#     store_items = iiko_cleint.casshift_sum_report(str_date, strn_date)
#     parse_si = ET.fromstring(store_items)
#     data_si = parse_si.findall('date')
#
#     for i in data_si:
#         document_id = i.find()
#         date = i.find('v/cls=java.util.Date типо такого')
#         number = i.find()
#         store = i.find('v/cls=java.lang.String')
#         amount = i.find()
#         diff = i.find()
#         surplus = i.find()
#         shortage = i.find()
#
#     table = """INSERT INTO overall_sales(document_id,date,number,store,amount,diff,surplus,shortage) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
#
#     for i in table:
#         c = conn.cursor()
#         c.execute(table, (document_id, date, number, store, amount, diff, surplus, shortage))
#         conn.commit()
#
# def get_emplshift ():
#     empl_shift = iiko_cleint.casshift_sum_report(str_date, strn_date)
#     parse_es = ET.fromstring(empl_shift)
#     data_es = parse_es.findall('date')
#
#     for i in data_es:
#         id_emp = i.find('v/cls=java.util.Date типо такого')
#         department_id = i.find('v/cls=java.lang.String')
#         date = i.find('v/cls=java.math.BigDecimal')
#         department_name = i.find('v/cls=java.math.BigDecimal')
#     table = """INSERT INTO empl_shift(date,department_id,department_name,id_emp) VALUES(%s,%s,%s,%s)"""
#
#     for i in table:
#         c = conn.cursor()
#         c.execute(table, (date, department_id, department_name, id_emp))
#         conn.commit()
call_aggr_sales = get_aggrsales()

