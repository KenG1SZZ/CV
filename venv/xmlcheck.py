import xml.etree.ElementTree as ET
import requests
import mysql.connector
from mysql import connector
import datetime
from datetime import date, timedelta
import time

conn = connector.connect(user='root',
                         password='erlan1990',
                         host='127.0.0.1',
                         database='bb_dashboard',
                         auth_plugin='mysql_native_password')
tree = ET.parse('responseOverall.xml')
