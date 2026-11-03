import json
import os

import requests
from dotenv import load_dotenv


class IpAddress:
    """Определяет ip-адрес пользователя с помощью сервиса ipify"""

    url_ip = "https://api.ipify.org/?format=json"
    timeout = 10

    def get_ip(self) -> str:
        """Функция для определения ip-адреса"""
        response = requests.get(self.url_ip, timeout=self.timeout)
        response.raise_for_status()
        return response.json()["ip"]


class GeoLocator:
    """Определяет геопозицию пользователя с помощью сервиса ipinfo"""

    timeout = 10

    def __init__(self):
        self.ip_address = IpAddress()

    def get_location(self) -> dict:
        """Функция для получения данных о местоположении текущего ip-адреса"""
        ip = self.ip_address.get_ip()
        url = f"https://ipinfo.io/{ip}/geo"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


class YD:
    """Клиент для работы с REST API Яндекс.Диска"""

    base_url = "https://cloud-api.yandex.net"
    timeout = 10

    def __init__(self, token: str):
        self._headers = {"Authorization": f"OAuth {token}"}

    def create_folder(self, path_new_folder: str = "/Location_student") -> None:
        """Создание новой папки в Яндекс.Диске"""
        response = requests.put(
            f"{self.base_url}/v1/disk/resources",
            params={"path": path_new_folder},
            headers=self._headers,
            timeout=self.timeout,
        )
        if response.status_code == 409:
            print(f"Папка '{path_new_folder}' уже существует")
            return
        response.raise_for_status()
        print(f"Папка '{path_new_folder}' создана")

    def get_link_for_upload(self, path_file: str) -> str:
        """Функция для получения ссылки для загрузки файла по указанному пути"""
        response = requests.get(
            f"{self.base_url}/v1/disk/resources/upload",
            params={"path": path_file, "overwrite": "true"},
            headers=self._headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["href"]

    def upload_json(self, data: dict, path_file: str) -> None:
        """Функция для загрузки JSON-данных по указанному пути на Яндекс.Диск"""
        href = self.get_link_for_upload(path_file)
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        response = requests.put(href, data=payload, timeout=self.timeout)
        response.raise_for_status()
        print(f"Файл по адресу: '{path_file}' успешно загружен")


def main() -> None:
    """Функция для вызова методов у класса. IP -> Geo -> JSON на Яндекс"""
    load_dotenv()
    token = os.getenv("TOKEN")

    if not token:
        raise RuntimeError("TOKEN не найден. Проверьте .env")

    geo_student = GeoLocator()
    geo_data = geo_student.get_location()

    student = YD(token)
    student.create_folder()
    student.upload_json(geo_data, "/Location_student/geo_student.json")


if __name__ == "__main__":
    main()
