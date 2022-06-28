# import xml element tree
import xml.etree.ElementTree as ET
import requests
# import mysql connector
from iiko_client import IikoClient
from iiko_auth import IikoServer
import datetime
from datetime import date, timedelta
import time


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

# get_aggr = iiko_cleint.casshift_by_aggregators(str_date, strn_date)
#get_inventory = iiko_cleint.inventory(str_date, strn_date)
#get_turnout =  iiko_cleint.turnout(str_date, strn_date)
get_overall = iiko_cleint.cashshift_sum_report(str_date, strn_date)

# while True:
#     try:
#         def get_oversales():
#
#
#         def get_aggrsales():
#
#
#         # def get_pricecost ():
#
#         # def get_storeitems():
#
#         # def get_emplshift ():
#         time.sleep(30)
#     except Exception as e:
#         print('exception error', e, end='\n\n#############################\n')


