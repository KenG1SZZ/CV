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


IIKO_URL = 'https://bahandi-co.iiko.it/resto/api'
IIKO_LOGIN = 'Keng1'
IIKO_PASSWORD = '37a7d5806f9d502b67bc96109eaa91918ac1d53b'

iiko_log = IIkoServer(IIKO_LOGIN, IIKO_PASSWORD, IIKO_URL)
IIKO_VERSION = iiko_log.get_version()
IIKO_TOKEN = iiko_log.auth()

iiko_cleint = IikoClient(IIKO_LOGIN, IIKO_PASSWORD, IIKO_URL, IIKO_VERSION, IIKO_TOKEN)
todaydate = date.today() - timedelta(days=1)
nextdate = date.today()
str_date = todaydate.strftime("%Y-%m-%d")
strn_date = nextdate.strftime("%Y-%m-%d")

def get_oversales ():

    overall_sales = iiko_cleint.casshift_sum_report(str_date)
    parse_overs = ET.fromstring(overall_sales)
    data_overs = parse_overs.findall('date')

    for i in data_overs:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('v/cls=java.lang.String')
        cash_sum = i.find('v/cls=java.math.BigDecimal')
    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()
def get_aggrsales ():

    aggr_sales = iiko_cleint.casshift_by_aggregators(str_date, strn_date)
    parse_aggr = ET.fromstring(aggr_sales)
    data_aggr = parse_aggr.findall('date')

    for i in data_aggr:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('k department v/cls=java.lang.String')
        paytype = i.find('k paytype v/cls=java.lang.String')
        cash_sum = i.find('v/cls=java.lang.BigDecimal')
    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()

def get_pricecost ():

    price_cost = iiko_cleint.cost_price(str_date, strn_date)
    parse_pcost = ET.fromstring(price_cost)
    data_overs = parse_pcost.findall('date')

    for i in data_overs:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('v/cls=java.lang.String')

        cash_sum = i.find('v/cls=java.math.BigDecimal')
    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()

def get_storeitems():
    overall_sales = iiko_cleint.casshift_sum_report(str_date, strn_date)
    parse_overs = ET.fromstring(overall_sales)
    data_overs = parse_overs.findall('date')

    for i in data_overs:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('v/cls=java.lang.String')
        cash_sum = i.find('v/cls=java.math.BigDecimal')
    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()

def get_emplshift ():
    overall_sales = iiko_cleint.casshift_sum_report(str_date, strn_date)
    parse_overs = ET.fromstring(overall_sales)
    data_overs = parse_overs.findall('date')

    for i in data_overs:
        date = i.find('v/cls=java.util.Date типо такого')
        department = i.find('v/cls=java.lang.String')
        cash_sum = i.find('v/cls=java.math.BigDecimal')
    table = """INSERT INTO overall_sales(date,department,cash_sum) VALUES(%s,%s,%s)"""

    for i in table:
        c = conn.cursor()
        c.execute(table, (date, department, cash_sum))
        conn.commit()
    #creating the cursor object


    # executing cursor object
# c.execute(data, (t_date, productName, productId,inted_v))

#######################################################
# token = None
# auth_url = 'https://bahandi-co.iiko.it/resto/api/'
# url = 'https://bahandi-co.iiko.it/resto/api/auth?login=' + IIKO_LOGIN + '&pass=' + IIKO_PASSWORD
# response = requests.get(url)
# if response.status_code == 200:
#     logout = requests.get('https://bahandi-co.iiko.it/api/logout?key=%s' % response.text).text
#     print(response.text)
# else:
#     time.sleep(30)
#     token = None
#     
# # todaydate = date.today()
# # str_date = todaydate.strftime("%d.%m.%Y")
# urlf = 'https://bahandi-co.iiko.it/resto/api/reports/productExpense?department=6fa71809-7b0e-44ae-aa79-62d44a75d32e&key=' + token +'&dateFrom=18.08.2021&dateTo=19.08.2021'
# response1 = requests.get(urlf)
# # in our xml file student is the root for all
# # student data.
# data2 = response1.text
# print(data2)
# # retrieving the data and insert into table
# # i value for xml data #j value printing number of
# # values that are stored
