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

    "--------------------------------------Общая сумма кассы и себестоимость-------------------------------------------"

    #     def cashshift_sum_report(self, pastdate, actualdate):
    #         str_date = pastdate + 'T23:59:59.999+06:00'
    #         n_date = actualdate + 'T23:59:59.999+06:00'
    #         payload = """<?xml version="1.0" encoding="utf-8"?>
    # <args>
    #     <client-type>BACK</client-type>
    #     <enable-warnings>false</enable-warnings>
    #     <client-call-id>9aa8e655-214f-4dbe-b8bb-71dcb0d4d459</client-call-id>
    #     <restrictions-state-hash>709</restrictions-state-hash>
    #     <obtained-license-connections-ids>81988994-ac58-4b8f-8734-56d956332cf6</obtained-license-connections-ids>
    #     <request-watchdog-check-results>true</request-watchdog-check-results>
    #     <use-raw-entities>true</use-raw-entities>
    #     <dateFrom>2022-05-01T00:00:00.000+06:00</dateFrom>
    #     <dateTo>2022-06-14T23:59:59.000+06:00</dateTo>
    #     <docType>SALES_DOCUMENT</docType>
    # </args>""" % (str_date, n_date)
    #
    #         try:
    #             response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
    #                                      headers=self.headers, data=payload)
    #             parse = ET.fromstring(response.content)
    #             for et in parse.iter("i"):
    #                 if len(data := et.findall("v")) == 4:
    #                     table = """INSERT INTO test(date,department,cash_sum,paytype) VALUES(%s,%s,%s,%s)"""
    #                     date, department, cash_sum, paytype = (x.text for x in data)
    #                     print(date, department, cash_sum, paytype)
    #                     c = conn.cursor()
    #                     c.execute(table, (date, department, cash_sum, paytype))
    #                     conn.commit()
    #             return response.content
    #         except Exception as e:
    #             return repr(e)

    "--------------------------------------Сумма кассы по аггрегаторам-------------------------------------------------"

    def casshift_by_aggregators(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
    <args>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <obtained-license-connections-ids>da370e44-0a82-438d-85f2-c9dd7b35fac8</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
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
        # '<from cls="java.util.Date">2022-05-01T00:00:00.000+06:00</from>
        #             <to cls="java.util.Date">2022-06-21T00:00:00.000+06:00</to>'
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

    "--------------------------------------Инвентеризация-------------------------------------------------"

    def storage_check(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <obtained-license-connections-ids>df254ac2-335b-4b1a-9059-36001ee09206</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <dateFrom>2022-06-01T00:00:00.000+06:00</dateFrom>
    <dateTo>2022-06-22T00:00:00.000+06:00</dateTo>
    <docType>INCOMING_INVENTORY</docType>
</args>"""
        # % (str_date, n_date)
        response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
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
            table: str = """INSERT INTO test(doc_id, date, doc, store_id, amount, sum, surplus, shortage) VALUES(%s,%s,
            %s,%s,%s,%s,%s,%s) """
            c = conn.cursor()
            c.execute(table, (doc_id, date, doc, store, amount, sum, surplus, shortage))
            conn.commit()

    "--------------------------------------Явки-------------------------------------------------"

    def employee_check(self, pastdate, actualdate):
        str_date = pastdate + 'T00:00:00.000+06:00'
        n_date = actualdate + 'T00:00:00.000+06:00'

        try:
            response = requests.get(
                self.host + '/resto/api/employees/attendance?from=%s&to=%s&withPaymentDetails=false&key=%s') % (
                           str_date, n_date, self.token)
            return response.content
        except Exception as e:
            return repr(e)
