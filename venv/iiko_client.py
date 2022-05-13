import requests
import datetime
from dicttoxml import dicttoxml

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
        if token:
            self.token
        else:
            self.auth()

    def auth(self):
        try:
            response = requests.get(self.host + '/resto/api/auth?login=' + self.login + '&pass=' + self.password)
            self.token = response.text
        except Exception as e:
            return repr(e)

    def verify(self):
        response = requests.get(self.host + '/resto/api/v2/entities/list?rootType=TaxCategory&key' + self.token)
        if response:
            return
        else:
            self.auth()

    def logout(self):
        try:
            response = requests.get(self.host + '/resto/api/logout?key=' + self.token)
            return response.text
        except Exception as e:
            return repr(e)

    "---------------------------------------------Общая сумма кассы--------------------------------------------------------------------------------------------------"

    def casshift_sum_report(self, actualdate):

        actualdate = date.today()
        str_date = actualdate.strftime("YYYY-MM-DD")
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <entities-version>20531613</entities-version>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>a12e9fd6-e951-4306-a893-88a75ace85ae</client-call-id>
    <license-hash>1932154536</license-hash>
    <restrictions-state-hash>11839</restrictions-state-hash>
    <obtained-license-connections-ids>ec54d1ba-c444-4cad-a4e2-68a50c45ab41</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList" />
    <groupByColFields cls="java.util.ArrayList" />
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
</args>""" % (str_date)
        headers = {

            'Content-Type': 'text/xml',
            'X-Resto-LoginName': 'Keng1',
            'X-Resto-PasswordHash': '37a7d5806f9d502b67bc96109eaa91918ac1d53b',
            'X-Resto-BackVersion': '7.9.7013.0',
            'Accept-Language': 'ru',
            'Host': 'bahandi-co.iiko.it',
            'Accept-Encoding': 'gzip',
            'Connection': 'Close'
            

        }
        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)
            return response.content
        except Exception as e:
            return repr(e)
    "--------------------------------------------Сумма кассы по аггрегаторам-----------------------------------------------------------------------------------------------"

    def casshift_by_aggregators(self, actualdate):
        actualdate = date.today()
        str_date = actualdate.strftime("YYYY-MM-DD")
        payload = """<?xml version="1.0" encoding="utf-8"?>
        <args>
            <entities-version>19980005</entities-version>
            <client-type>BACK</client-type>
            <enable-warnings>false</enable-warnings>
            <client-call-id>d9153d72-9a1d-452b-81a9-21375f87d87b</client-call-id>
            <license-hash>776916167</license-hash>
            <restrictions-state-hash>3040</restrictions-state-hash>
            <obtained-license-connections-ids>8bf2d3e1-9792-4d6a-9673-c0f1da8cc107</obtained-license-connections-ids>
            <request-watchdog-check-results>true</request-watchdog-check-results>
            <use-raw-entities>true</use-raw-entities>
            <olapReportType>SALES</olapReportType>
            <groupByRowFields cls="java.util.ArrayList">
                <i>Department</i>
                <i>PayTypes</i>
            </groupByRowFields>
            <groupByColFields cls="java.util.ArrayList" />
            <aggregateFields cls="java.util.ArrayList">
                <i>DishSumInt</i>
            </aggregateFields>
            <filters>
                <k>SessionID.OperDay</k>
                <v cls="FilterDateRangeCriteria">
                    <periodType>CURRENT_MONTH</periodType>
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
        </args>""" % (str_date)
        headers = {

            'Content-Type': 'text/xml',
            'X-Resto-LoginName': 'Keng1',
            'X-Resto-PasswordHash': '37a7d5806f9d502b67bc96109eaa91918ac1d53b',
            'X-Resto-BackVersion': '7.9.7013.0',
            'Accept-Language': 'ru',
            'Host': 'bahandi-co.iiko.it',
            'Accept-Encoding': 'gzip',
            'Connection': 'Close'

        }
        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)
            return response.content
        except Exception as e:
            return repr(e)


    "------------------------------------------------------Себестоимость-----------------------------------------------------------------------------------------------"

    def cost_price(self, actualdate):
        actualdate = date.today()
        str_date = actualdate.strftime("YYYY-MM-DD")
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <entities-version>20470108</entities-version>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>65632738-fdd3-4b53-9936-dcd04ff256d3</client-call-id>
    <license-hash>1120827031</license-hash>
    <restrictions-state-hash>9607</restrictions-state-hash>
    <obtained-license-connections-ids>4240e280-ff48-41c0-a245-5ddadf581648</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList" />
    <groupByColFields cls="java.util.ArrayList" />
    <aggregateFields cls="java.util.ArrayList">
        <i>ProductCostBase.ProductCost</i>
    </aggregateFields>
    <filters>
        <k>SessionID.OperDay</k>
        <v cls="FilterDateRangeCriteria">
            <periodType>CUSTOM</periodType>
            <from cls="java.util.Date">2022-05-10T00:00:00.000+06:00</from>
            <to cls="java.util.Date">2022-05-12T00:00:00.000+06:00</to>
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
</args>""" % (str_date)
        headers = {

            'Content-Type': 'text/xml',
            'X-Resto-LoginName': 'Keng1',
            'X-Resto-PasswordHash': '37a7d5806f9d502b67bc96109eaa91918ac1d53b',
            'X-Resto-BackVersion': '7.9.7013.0',
            'Accept-Language': 'ru',
            'Host': 'bahandi-co.iiko.it',
            'Accept-Encoding': 'gzip',
            'Connection': 'Close'

        }
        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)
            return response.content
        except Exception as e:
            return repr(e)



    "-----------------------------------------------------------Инвентеризация----------------------------------------------------------------------------------------------"

    def storage_check(self, actualdate):
        actualdate = date.today()
        str_date = actualdate.strftime("YYYY-MM-DD")
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <entities-version>20465128</entities-version>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>12257b40-1366-448f-bf66-f34f1356855d</client-call-id>
    <license-hash>1120827031</license-hash>
    <restrictions-state-hash>9441</restrictions-state-hash>
    <obtained-license-connections-ids>df254ac2-335b-4b1a-9059-36001ee09206</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <dateFrom>%s</dateFrom>
    <dateTo>%s</dateTo>
    <docType>INCOMING_INVENTORY</docType>
</args>""" % (str_date)
        headers = {

            'Content-Type': 'text/xml',
            'X-Resto-LoginName': 'Keng1',
            'X-Resto-PasswordHash': '37a7d5806f9d502b67bc96109eaa91918ac1d53b',
            'X-Resto-BackVersion': '7.9.7013.0',
            'Accept-Language': 'ru',
            'Host': 'bahandi-co.iiko.it',
            'Accept-Encoding': 'gzip',
            'Connection': 'Close'

        }
        try:
            response = requests.post(self.host + '/resto/services/olapReport?methodName=buildReport',
                                     headers=self.headers, data=payload)
            return response.content
        except Exception as e:
            return repr(e)

    "--------------------------------------------------------------Явки----------------------------------------------------------------------------------------------------"

    def employee_check(self, actualdate):
        actualdate = date.today()
        str_date = actualdate.strftime("YYYY-MM-DD")

        try:
            response = requests.get(self.host + '/resto/api/employees/attendance?from=%s&to=%s&withPaymentDetails=false&key=%s') % (
            str_date, str_date, self.token
        )
            return response.content
        except Exception as e:
            return repr(e)

