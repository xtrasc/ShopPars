from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


class MetroParsing:
    def __init__(self, url):
        # Настройки
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

        self.url = url
        self.products = []
        self.alias_name = "Кофе"
    def open_page(self):
        self.driver.get(self.url)
        time.sleep(5)

    def extract_alias_name(self):
        """Извлечь название категории"""
        try:
            alias_element = self.driver.find_element(By.CLASS_NAME, "subcategory-or-type__heading-title")
            self.alias_name = alias_element.text
            print(f"Категория: {self.alias_name}")
        except Exception as e:
            print(f"Ошибка при извлечении названия категории: {e}")

    def load_more_products(self):
        a = 0
        while a < 7:
            try:
                wait = WebDriverWait(self.driver, 1)
                load_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div/div/div[3]/div[1]/main/div[2]/button")))
                load_more_button.click()
                time.sleep(5)
                a += 1
            except Exception as e:
                print(f"Ошибка при загрузке дополнительных товаров: {e}")
                break

    def extract_product_data(self):
        product_elements = self.driver.find_elements(By.CLASS_NAME, "catalog-2-level-product-card")
        print(f"Найдено карточек товаров: {len(product_elements)}")

        for element in product_elements:
            try:
                name = element.find_element(By.CLASS_NAME, "product-card-name__text").text
                price_with_discount = self.get_price_with_discount(element)
                price_without_discount = self.get_price_without_discount(element)
                brand = self.get_brand(name)
                id = self.get_product_id(element)
                link = self.get_product_link(element)

                self.products.append({
                    "name": name,
                    "alias":self.alias_name,
                    "id": id,
                    "price_with_discount": price_with_discount,
                    "price_without_discount": price_without_discount,
                    "brand": brand,
                    "url": link
                })
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

    def get_price_with_discount(self, element):
        "Получить цену со скидкой"
        try:
            return element.find_element(By.CLASS_NAME, "product-price__sum-rubles").text
        except:
            return "Нет скидки"

    def get_price_without_discount(self, element):
        "Получить цену без скидки"
        try:
            return element.find_element(By.CLASS_NAME, "product-unit-prices__old-wrapper").text
        except:
            return "Нет старой цены"

    def get_brand(self, name):
        "Получить бренд товара"
        try:
            return name[:18]  # Предположим, что бренд состоит из первых 18 символов имени
        except:
            return "Не указано"

    def get_product_id(self, element):
        """Получить ID товара"""
        try:
            return element.get_attribute("id")
        except:
            return "Ошибка"

    def get_product_link(self, element):
        "Получить ссылку на товар"
        try:
            link = element.find_element(By.CLASS_NAME, "product-card-name")
            return link.get_attribute("href")
        except:
            return "Нет ссылки"

    def save_data_to_json(self, filename="metro_coffee.json"):
        "Сохранить данные о товарах в JSON файл"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")

    def close_driver(self):
        self.driver.quit()



if __name__ == "__main__":
    url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search"

    scraper = MetroParsing(url)
    scraper.open_page()
    scraper.load_more_products()  # Подгружаем больше товаров
    scraper.extract_product_data()  # Извлекаем данные о товарах
    scraper.save_data_to_json()  # Сохраняем данные в файл
    scraper.close_driver()  # Закрываем браузер
