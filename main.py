import re
import socket
from typing import Optional

import requests


class SiteChecker:
    def __init__(self, url: str):
        """
        Инициализация класса с URL сайта.

        :param url: URL сайта для проверки.
        """
        self.url = url
        self.ip_address: Optional[str] = None

    def check_site_availability(self) -> requests.Response:
        """
        Проверяет доступность сайта.

        :return: Объект Response при успешном доступе.
        :raises ConnectionError: Ошибка подключения к сайту.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при доступе к сайту: {e}")

    def fetch_ip_address(self) -> None:
        """
        Получает IP-адрес сайта.

        :raises ConnectionError: Ошибка при получении IP-адреса.
        """
        try:
            hostname = self.url.replace('http://', '').replace('https://', '').split('/')[0]
            self.ip_address = socket.gethostbyname(hostname)
        except socket.gaierror as e:
            raise ConnectionError(f"Ошибка при получении IP-адреса: {e}")

    def find_phone_number(self, webpage_content: str) -> str:
        """
        Ищет телефонный номер на веб-странице.

        :param webpage_content: HTML содержимое веб-страницы.
        :return: Форматированный телефонный номер.
        :raises ValueError: Телефонный номер на сайте не найден.
        """
        phone_pattern = r"(?:\+(\d{1,3}))?\s*\(?(\d{3,5})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        phone_match = re.search(phone_pattern, webpage_content)
        if phone_match:
            country_code = phone_match.group(1) if phone_match.group(1) else "8"
            formatted_phone_number = f"{country_code}({phone_match.group(2)}){phone_match.group(3)}-{phone_match.group(4)}-{phone_match.group(5)}"
            return formatted_phone_number
        else:
            raise ValueError("Телефонный номер на сайте не найден.")

    def validate_phone_number(self, phone_number: str) -> str:
        """
        Проверяет телефонный номер на соответствие заданному формату.

        :param phone_number: Форматированный телефонный номер.
        :return: Допустимый телефонный номер.
        :raises ValueError: Номер телефона не соответствует стандарту.
        """
        valid_phone_pattern = r"^(\+?\d{1,3})?\(?\d{1,5}\)?\d{1,3}-\d{2}-\d{2}$"
        if not re.match(valid_phone_pattern, phone_number):
            raise ValueError("Найденный номер телефона не соответствует стандарту.")
        return phone_number

    def run_checks(self) -> str:
        """
        Запускает все проверки.

        :return: Строка с результатами проверок.
        """
        response = self.check_site_availability()
        self.fetch_ip_address()
        phone_number = self.find_phone_number(response.text)
        valid_phone = self.validate_phone_number(phone_number)
        return f"IP адрес: {self.ip_address}, Допустимый номер телефона: {valid_phone}"


# Пример использования класса
if __name__ == "__main__":
    checker = SiteChecker("http://sstmk.ru")
    try:
        result = checker.run_checks()
        print(result)
    except Exception as e:
        print(e)
