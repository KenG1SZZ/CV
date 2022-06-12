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
            'X-Resto-BackVersion': '',
            'X-Resto-AuthType': 'BACK',
            'X-Resto-ServerEdition': 'IIKO_CHAIN',
            'Host': host.replace('http://', '').replace('https://', ''),
            'Content-Type': 'application/xml',
            'Content-Length': '875'
        }
        self.token = token

    "---------------------------------------------Общая сумма кассы--------------------------------------------------------------------------------------------------"

    def casshift_sum_report(self, pastdate, actualdate):
        str_date = pastdate + 'T23:59:59.999+06:00'
        n_date = actualdate + 'T23:59:59.999+06:00'
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
</args>""" % (str_date, n_date)
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

    def casshift_by_aggregators(self, pastdate, actualdate):
        str_date = pastdate + 'T23:59:59.999+06:00'
        n_date = actualdate + 'T23:59:59.999+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <entities-version>21772951</entities-version>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>ae7ea071-adab-41c2-8435-ce7368e201b8</client-call-id>
    <license-hash>-261807956</license-hash>
    <restrictions-state-hash>18295</restrictions-state-hash>
    <obtained-license-connections-ids>7557e22d-4a2a-4985-938a-225d3eb3faf1</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <olapReportType>SALES</olapReportType>
    <groupByRowFields cls="java.util.ArrayList">
        <i>Department</i>
        <i>OpenDate.Typed</i>
        <i>PayTypes</i>
    </groupByRowFields>
    <groupByColFields cls="java.util.ArrayList"/>
    <aggregateFields cls="java.util.ArrayList">
        <i>DishSumInt</i>
    </aggregateFields>
    <filters>
        <k>SessionID.OperDay</k>
        <v cls="FilterDateRangeCriteria">
            <periodType>CURRENT_MONTH</periodType>
            <from cls="java.util.Date">2022-06-01T00:00:00.000+06:00</from>
            <to cls="java.util.Date">2022-07-01T00:00:00.000+06:00</to>
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
</args>""" % (str_date, next_date)
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

    def cost_price(self, pastdate, actualdate):
        str_date = pastdate + 'T23:59:59.999+06:00'
        n_date = actualdate + 'T23:59:59.999+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>37e10490-dce4-4e98-8b14-8eb5128c1bd6</client-call-id>
    <obtained-license-connections-ids>cf56a52d-9e69-4c40-9f3b-d28095f0459b</obtained-license-connections-ids>
    <request-watchdog-check-results>false</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
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
            <periodType>CURRENT_MONTH</periodType>
            <from cls="java.util.Date">2022-05-01T00:00:00.000+06:00</from>
            <to cls="java.util.Date">2022-06-01T00:00:00.000+06:00</to>
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
</args>""" % (str_date, next_date)
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

    def storage_check(self, pastdate, actualdate):
        str_date = pastdate + 'T23:59:59.999+06:00'
        n_date = actualdate + 'T23:59:59.999+06:00'
        payload = """<?xml version="1.0" encoding="utf-8"?>
<args>
    <entities-version>20691806</entities-version>
    <client-type>BACK</client-type>
    <enable-warnings>false</enable-warnings>
    <client-call-id>1c89bded-da56-45c6-b042-1e69b64bc044</client-call-id>
    <license-hash>-1204008798</license-hash>
    <restrictions-state-hash>16434</restrictions-state-hash>
    <obtained-license-connections-ids>e0689d2e-4fe8-4f6e-9160-dd1f685e6f3d</obtained-license-connections-ids>
    <request-watchdog-check-results>true</request-watchdog-check-results>
    <use-raw-entities>true</use-raw-entities>
    <dateFrom>%s</dateFrom>
    <dateTo>%s</dateTo>
    <docType>INCOMING_INVENTORY</docType>
</args>""" % (str_date, next_date)
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

    def employee_check(self, pastdate, actualdate):
        str_date = pastdate + 'T23:59:59.999+06:00'
        n_date = actualdate + 'T23:59:59.999+06:00'

        try:
            response = requests.get(
                self.host + '/resto/api/employees/attendance?from=%s&to=%s&withPaymentDetails=false&key=%s') % (
                       str_date, next_date, self.token)
            return response.content
        except Exception as e:
            return repr(e)
