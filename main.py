
import requests

import requests
from dotenv import load_dotenv

load_dotenv()

class IpAdress:
    """Определяет ip-адресс пользователя с помощью сервиса ipify"""

    url_ip = 'https://api.ipify.org/?format=json'
    timeout = 10

    def _get_ip(self) -> str:
        """Функция для определения ip-адреса"""

        response = requests.get(self.url_ip, timeout=self.timeout)
        response.raise_for_status()
        return response.json()['ip']

