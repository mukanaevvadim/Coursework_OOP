
import os
import requests

from dotenv import load_dotenv

load_dotenv()

class IpAddress:
    """Определяет ip-адрес пользователя с помощью сервиса ipify"""

    url_ip = 'https://api.ipify.org/?format=json'
    timeout = 10

    def get_ip(self) -> str:
        """Функция для определения ip-адреса"""

        response = requests.get(self.url_ip, timeout=self.timeout)
        response.raise_for_status()
        return response.json()['ip']


class GeoLocator:
    """Определяет геопозицию пользователя с помощью сервиса ipinfo"""
    timeout = 10

    def __init__(self):
        self.ip_address = IpAddress()

    def get_location(self) -> dict:
        """Функция для получения данных о местоположении текущего ip-адреса"""
        ip = self.ip_address.get_ip()
        url = f'https://ipinfo.io/{ip}/geo'
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    geo_student = GeoLocator()
    print(geo_student.get_location())