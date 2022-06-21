import requests
from lxml import etree
from io import StringIO


class IikoServer:

    def __init__(self, host: str, login: str, password: str):
        self.host = host
        self.login = login
        self.password = password
        self.token = None

    def get_version(self):
        try:
            ver = requests.get(
                  self.host + '/resto/get_server_info.jsp?encoding=UTF-8')
            strgln = ver.text
            tree = etree.parse(StringIO(strgln))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def auth(self):
        try:
            response = requests.get(self.host + '/resto/api/auth?login=' + self.login + '&pass=' + self.password)
            return response.text

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
