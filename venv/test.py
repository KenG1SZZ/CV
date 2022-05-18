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

conn = connector.connect(user='root',
                         password='erlan1990e',
                         host='127.0.0.1',
                         database='daily_report',
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


iiko_cleint = IikoClient(IIKO_LOGIN, IIKO_PASSWORD, IIKO_URL)
todaydate = date.today() - timedelta(days=1)
str_date = todaydate.strftime("%Y-%m-%d")

overall_sales = iiko_cleint.casshift_sum_report(str_date)
aggr_sales = iiko_cleint.casshift_by_aggregators(str_date)
price_cost = iiko_cleint.cost_price(str_date)
str_items = iiko_cleint.storage_check(str_date)
empl_shift = iiko_cleint.employee_check(str_date)

parse_overs = ET.fromstring(overall_sales)
parse_avgs = ET.fromstring(aggr_sales)
parse_pcost = ET.fromstring(price_cost)
parse_items = ET.fromstring(str_items)
parse_empls = ET.fromstring(empl_shift)


data_overs = parse_overs.findall('data')



orders = orderdata[0].text
avg_check = data_avg[0].text
cash_sum = data_sum[0].text
pr_id = data_prc[0].text
pr_amount = amount[0].text
pr_price = prod_price[0].text
pr_supplier = supplier[0].text

#print(iiko_cleint.get_consumption('6fa71809-7b0e-44ae-aa79-62d44a75d32e', str_ydate, str_date))
#print(data_c)
#print(cash_sum)
#print(avg_check)
for ep in data_c:
     t_date = ep.find('date')
     f_date = datetime.datetime.strptime(t_date.text,"%d.%m.%Y").strftime("%Y-%m-%d")
     productName = ep.find('productName').text
     productId = ep.find('productId').text
     value = float(ep.find('value').text)
     inted_v = value
     # print(productName)
     data = """INSERT INTO cons_by_sales(date,productName,productId,value) VALUES(%s,%s,%s,%s)"""

for i in data:
     #print("asdf")
#data = """SELECT * from cons_by_sales"""
     c = conn.cursor()
     c.execute(data, (f_date, productName, productId, inted_v))
     conn.commit()

# for i in orderdata:
#     orders = i.find('').text
#     print(orders)




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
