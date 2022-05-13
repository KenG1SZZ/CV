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
                         password='asdbkb123321',
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
IIKO_LOGIN = 'BB_Salary'
IIKO_PASSWORD = 'a2db784ded68d5a827b2c3690e9fa5131eedf322'


iiko_cleint = IikoClient(IIKO_LOGIN, IIKO_PASSWORD, IIKO_URL)
todaydate = date.today() - timedelta(days=1)
str_date = todaydate.strftime("%d.%m.%Y")

consumption = iiko_cleint.get_consumption(str_date, str_date)
get_sales = iiko_cleint.sales(str_date, str_date)
get_avg = iiko_cleint.avg_inv(str_date, str_date)
get_sum = iiko_cleint.allsum(str_date, str_date)
get_com = iiko_cleint.take_com(str_date, str_date)

parse_sum = ET.fromstring(get_sum)
parse_c = ET.fromstring(consumption)
parse_sales = ET.fromstring(get_sales)
parse_avg = ET.fromstring(get_avg)
parse_com = ET.fromstring(get_com)


data_sum = parse_sum.findall('r/DishDiscountSumInt')
prod_id = parse_com.findall('r/product')
supplier = parse_com.findall('r/supplier')
amount = parse_com.findall('r/amount')
prod_price = parse_c.findall('r/price')
prod_sum = parse_c.findall('r/sum')
data_avg = parse_avg.findall('r/DishDiscountSumInt.average')
com_data = parse_prc.findall('')
orderdata = parse_sales.findall('r/UniqOrderId.OrdersCount')

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
