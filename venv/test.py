# import xml element tree
import xml.etree.ElementTree as ET
import requests
# import mysql connector
from iiko_client import IikoClient
from iiko_auth import IikoServer
import datetime
from datetime import date, timedelta
import time
from time import sleep

IIKO_URL = 'https://bahandi-co.iiko.it'
IIKO_LOGIN = 'Keng1'
IIKO_PASSWORD = '37a7d5806f9d502b67bc96109eaa91918ac1d53b'

iiko_log = IikoServer(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD)
IIKO_VERSION = iiko_log.get_version()
IIKO_TOKEN = iiko_log.auth()

iiko_cleint = IikoClient(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD, IIKO_VERSION, IIKO_TOKEN)
todaydate = date.today() - timedelta(days=1)
nextdate = date.today()
futuredate = date.today() + timedelta(days=1)
str_date = todaydate.strftime("%Y-%m-%d")
strn_date = nextdate.strftime("%Y-%m-%d")
strf_date = futuredate.strftime("%Y-%m-%d")


def LoopforSQL():
    while True:
        get_aggr = iiko_cleint.casshift_by_aggregators(str_date, strn_date)

        get_inventory = iiko_cleint.inventory(str_date, strn_date)

        get_turnout = iiko_cleint.turnout(strn_date, strf_date)

        get_overall = iiko_cleint.sales_by_day(str_date, strn_date)

        get_costp = iiko_cleint.cashshift_report(str_date, strn_date)

        time.sleep(35)


class Pythonservice(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PBItoMYSQL'
    _svc_display_name_ = 'PTM'
    _svc_description_ = 'Service for transferring data from IIKO to MYSQL and Then to PBI'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        LoopforSQL()


if __name__ == '__main__':
    Pythonservice.parse_command_line()
