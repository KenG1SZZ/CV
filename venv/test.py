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
import schedule

IIKO_URL = 'https://bahandi-co.iiko.it'
IIKO_LOGIN = 'Keng1'
IIKO_PASSWORD = '48efc4851e15940af5d477d3c0ce99211a70a3be'

iiko_log = IikoServer(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD)
IIKO_VERSION = iiko_log.get_version()
IIKO_TOKEN = iiko_log.auth()

iiko_cleint = IikoClient(IIKO_URL, IIKO_LOGIN, IIKO_PASSWORD, IIKO_VERSION, IIKO_TOKEN)
todaydate = date.today()
nextdate = date.today() + timedelta(days=1)
futuredate = date.today() - timedelta(days=1)
str_date = todaydate.strftime("%Y-%m-%d")
strn_date = nextdate.strftime("%Y-%m-%d")
strf_date = futuredate.strftime("%Y-%m-%d")


def job():
    get_aggr = iiko_cleint.casshift_by_aggregators(str_date, strn_date)

    get_inventory = iiko_cleint.inventory(str_date, strn_date)

    get_turnout = iiko_cleint.turnout(strn_date, strf_date)

    get_overall = iiko_cleint.sales_by_day(str_date, strn_date)

    get_costp = iiko_cleint.cashshift_report(str_date, strn_date)


schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
