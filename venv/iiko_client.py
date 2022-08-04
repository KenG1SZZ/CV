from typing import Union, Any

import requests
import datetime
from dicttoxml import dicttoxml
import mysql.connector
from mysql import connector
import xml.etree.ElementTree as ET

from mysql.connector import CMySQLConnection, MySQLConnection

conn: Union[Union[CMySQLConnection, MySQLConnection], Any] = connector.connect(user='root',
                                                                               password='erlan1990',
                                                                               host='localhost',
                                                                               database='bahandireport',
                                                                               auth_plugin='mysql_native_password')


class IikoClient:
    host: str = None
    login: str = None
    password: str = None
    version: str = None
    headers: dict = {}
    token: str = None

    def __init__(self, host: str, login: str, password: str, version: str, token: str):

        self.host = host
        self.login = login
        self.password = password
        self.version = version
        self.headers = {
            'X-Resto-LoginName': login,
            'X-Resto-PasswordHash': password,
            'X-Resto-BackVersion': version,
            'X-Resto-AuthType': 'BACK',
            'X-Resto-ServerEdition': 'IIKO_CHAIN',
            'Host': host.replace('http://', '').replace('https://', ''),
            'Content-Type': 'application/xml',
            'Content-Length': '875'
        }
        self.token = token

    "--------------------------------------Касса в день -----------------------------------------------"

    def sales_by_day(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList">
        <i>OpenDate.Typed</i>
    </groupByRowFields>
    <groupByColFields cls="java.util.ArrayList">
        <i>Department</i>
    </groupByColFields>
    <aggregateFields cls="java.util.ArrayList">
        <i>DishSumInt</i>
    </aggregateFields>
    <filters>
        <k>SessionID.OperDay</k>
        <v cls="FilterDateRangeCriteria">
            <periodType>CUSTOM</periodType>
            <from cls="java.util.Date">%s</from>
            <to cls="java.util.Date">%s</to>
            <includeLow>true</includeLow>
            <includeHigh>false</includeHigh>
        </v>
        <k>DeletedWithWriteoff</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="DishDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
        <k>OrderDeleted</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="OrderDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
    </filters>
</args>""" \
                   % (str_date, n_date)

        response = requests.post(
            self.host + '/resto/services/olapReport?methodName=buildReport',
            headers=self.headers, data=payload)
        parse_aggr = ET.fromstring(response.content)
        try:
            for et in parse_aggr.iter("i"):
                if len(data := et.findall("v")) == 3:
                    table = """INSERT INTO sales_by_day(date,department,sales) VALUES(%s,%s,%s)"""
                    date, department, sales = (x.text for x in data)
                    print(date, department, sales)
                    c = conn.cursor()
                    c.execute(table, (date, department, sales))
                    conn.commit()

        except Exception as e:
            print('exception error   ', e, end='\n\n#############################\n')
            error_handle = """INSERT INTO sales_by_day
  (department, date, sales)
SELECT
   'test', NULL, '1'
FROM
  dual
WHERE NOT EXISTS
      ( SELECT *  FROM bahandireport.sales_by_day  WHERE (sales, department) = ('1', 'test') )
  AND NOT EXISTS
      ( SELECT *  FROM bahandireport.sales_by_day  WHERE (department, date) = ('test',NULL) ) ;
      """
            c = conn.cursor()
            c.execute(error_handle)
            conn.commit()

    "-----------------------------------Себестоимость -------------------------------------------------------------------"

    def cashshift_report(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList">
        <i>Department</i>
    </groupByRowFields>
    <groupByColFields cls="java.util.ArrayList">
        <i>OpenDate.Typed</i>
    </groupByColFields>
    <aggregateFields cls="java.util.ArrayList">
        <i>ProductCostBase.ProductCost</i>
    </aggregateFields>
    <filters>
        <k>SessionID.OperDay</k>
        <v cls="FilterDateRangeCriteria">
            <periodType>CUSTOM</periodType>
            <from cls="java.util.Date">%s</from>
            <to cls="java.util.Date">%s</to>
            <includeLow>true</includeLow>
            <includeHigh>false</includeHigh>
        </v>
        <k>DeletedWithWriteoff</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="DishDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
        <k>OrderDeleted</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="OrderDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
    </filters>
</args>""" % (str_date, n_date)

        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)
            parse_aggr = ET.fromstring(response.content)
            for et in parse_aggr.iter("i"):
                if len(data := et.findall("v")) == 3:
                    table = """INSERT INTO cost_price(date,department,cost_price) VALUES(%s,%s,%s)"""
                    date, department, cost_price = (x.text for x in data)
                    print(date, department, cost_price)
                    c = conn.cursor()
                    c.execute(table, (date, department, cost_price))
                    conn.commit()

        except Exception as e:
            print('exception error   ', e, end='\n\n#############################\n')
            error_handle = """INSERT INTO bahandireport.cost_price
  (date, department, cost_price)
SELECT
  NULL, 'test', '1'
FROM
  dual
WHERE NOT EXISTS
      ( SELECT *  FROM bahandireport.cost_price  WHERE (cost_price, department) = ('1', 'test') )
  AND NOT EXISTS
      ( SELECT *  FROM bahandireport.cost_price  WHERE (department, date) = ('test', NULL) ) ;"""
            c = conn.cursor()
            c.execute(error_handle)
            conn.commit()

    "--------------------------------------Сумма кассы по аггрегаторам-------------------------------------------------"

    def casshift_by_aggregators(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList">
        <i>OpenDate.Typed</i>
        <i>Department</i>
        <i>PayTypes</i>
    </groupByRowFields>
    <groupByColFields cls="java.util.ArrayList"/>
    <aggregateFields cls="java.util.ArrayList">
        <i>DishSumInt</i>
    </aggregateFields>
    <filters>
        <k>SessionID.OperDay</k>
        <v cls="FilterDateRangeCriteria">
            <periodType>CUSTOM</periodType>
            <from cls="java.util.Date">%s</from>
            <to cls="java.util.Date">%s</to>
            <includeLow>true</includeLow>
            <includeHigh>false</includeHigh>
        </v>
        <k>DeletedWithWriteoff</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="DishDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
        <k>OrderDeleted</k>
        <v cls="FilterIncludeValuesCriteria">
            <values>
                <i cls="OrderDeletionStatus">NOT_DELETED</i>
            </values>
        </v>
    </filters>
</args>""" % (str_date, n_date)
        # '<from cls="java.util.Date">2022-07-24T00:00:00.000+06:00</from>
        #    <to cls="java.util.Date">2022-08-02T00:00:00.000+06:00</to>'
        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)

            parse_aggr = ET.fromstring(response.content)

            for et in parse_aggr.iter("i"):
                if len(data := et.findall("v")) == 4:
                    table = """INSERT INTO aggr_sales(date,department,cash_sum,paytype) VALUES(%s,%s,%s,%s)"""
                    date, department, cash_sum, paytype = (x.text for x in data)
                    print(date, department, cash_sum, paytype)
                    c = conn.cursor()
                    c.execute(table, (date, department, cash_sum, paytype))
                    conn.commit()

        except Exception as e:
            print('exception error   ', e, end='\n\n#############################\n')
            error_handle = """INSERT INTO aggr_sales
  (date, department, cash_sum, paytype)
SELECT
  NULL, 'test', '1', 'test1'
FROM
  dual
WHERE NOT EXISTS
      ( SELECT *  FROM bahandireport.aggr_sales  WHERE (cash_sum, department) = ('1', 'test') )
  AND NOT EXISTS
      ( SELECT *  FROM bahandireport.aggr_sales  WHERE (department, paytype) = ('test', 'test1') ) ;
      """
            c = conn.cursor()
            c.execute(error_handle)
            conn.commit()

    "--------------------------------------Инвентеризация-------------------------------------------------"

    def inventory(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <dateFrom>%s</dateFrom>
    <dateTo>%s</dateTo>
    <docType>INCOMING_INVENTORY</docType>
</args>""" % (str_date, n_date)
        try:
            response = requests.post(
                self.host + '/resto/services/document?methodName=getIncomingDocumentsRecordsByDepartments',
                headers=self.headers, data=payload)
            parse = ET.fromstring(response.content)
            parse_str = parse.find('returnValue')
            for i in parse_str.iter("i"):
                doc_id = i.find('documentID').text
                date = i.find('date').text
                doc = i.find('documentSummary').text
                store = i.find('storeFrom').text
                amount = i.find('amount').text
                sum = i.find('sum').text
                surplus = i.find('surplusSum').text
                shortage = i.find('shortageSum').text
                print(doc_id, date, doc, store, amount, sum, surplus, shortage)
                table: str = """INSERT INTO inventory(doc_id, date, doc, store_id, amount, sum, surplus, shortage) VALUES(%s,%s,
                        %s,%s,%s,%s,%s,%s) """
                c = conn.cursor()
                c.execute(table, [doc_id, date, doc, store, amount, sum, surplus, shortage])
                conn.commit()
        except Exception as e:
            print('exception error   ', e, end='\n\n#############################\n')
            error_handle = """Insert into inventory(store_id) values('') on duplicate key update doc_id = doc_id"""
            c = conn.cursor()
            c.execute(error_handle)
            conn.commit()

    "--------------------------------------Явки-------------------------------------------------"

    def turnout(self, pastdate, actualdate):
        str_date = pastdate
        n_date = actualdate
        try:
            response = requests.get(
                self.host + '/resto/api/employees/attendance?from=' + str_date + '&to=' + n_date + '&withPaymentDetails=false&key=' + self.token)
            parse = ET.fromstring(response.content)
            for i in parse.iter("attendance"):
                doc_id = i.find('id').text
                date = i.find('dateFrom').text
                if (date < str_date or date > n_date):
                    continue
                employee_id = i.find('employeeId').text
                department_id = i.find('departmentId').text
                department_name = i.find('departmentName').text
                print(doc_id, employee_id, date, department_id, department_name)
                table: str = """INSERT INTO turnout_table(doc_id, employee_id, date, department_id, 
                        department_name) VALUES(%s,%s,%s,%s,%s) """
                c = conn.cursor()
                c.execute(table, (doc_id, employee_id, date, department_id, department_name))
                conn.commit()

        except Exception as e:
            print('exception error   ', e, end='\n\n#############################\n')
            error_handle = """Insert into turnout_table(department_name) values('') on duplicate key update doc_id = doc_id"""
            c = conn.cursor()
            c.execute(error_handle)
            conn.commit()
