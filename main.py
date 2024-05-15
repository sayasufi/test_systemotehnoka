import requests
import re
import socket

class SiteChecker:
    def __init__(self, url):
        self.url = url
        self.ip_address = None

    def check_site_availability(self):
        """Проверяет доступность сайта."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при доступе к сайту: {e}")

    def fetch_ip_address(self):
        """Получает IP-адрес сайта."""
        try:
            hostname = self.url.replace('http://', '').replace('https://', '').split('/')[0]
            self.ip_address = socket.gethostbyname(hostname)
        except socket.gaierror as e:
            raise ConnectionError(f"Ошибка при получении IP-адреса: {e}")

    def find_phone_number(self, webpage_content):
        """Ищет телефонный номер на веб-странице."""
        phone_pattern = r"(\+?\d{1,3})?\s*\(?(\d{3,5})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        phone_match = re.search(phone_pattern, webpage_content)
        if phone_match:
            # Форматируем номер телефона в желаемый формат
            country_code = phone_match.group(1) if phone_match.group(1) else "+7"
            formatted_phone_number = f"{country_code}({phone_match.group(2)}){phone_match.group(3)}-{phone_match.group(4)}-{phone_match.group(5)}"
            return formatted_phone_number
        else:
            raise ValueError("Телефонный номер на сайте не найден.")

    def validate_phone_number(self, phone_number):
        """Проверяет телефонный номер на соответствие заданному формату."""
        valid_phone_pattern = r"^(\+?\d{1,3})?\(?\d{1,5}\)?\d{1,3}-\d{2}-\d{2}$"
        if not re.match(valid_phone_pattern, phone_number):
            raise ValueError("Найденный номер телефона не соответствует стандарту.")
        return phone_number

    def run_checks(self):
        """Запускает все проверки."""
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
