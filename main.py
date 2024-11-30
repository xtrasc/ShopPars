from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Настройки для Selenium
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Запуск браузера в фоновом режиме
driver = webdriver.Chrome(options=options)

# URL категории
url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search"
driver.get(url)

# Ожидание загрузки страницы
time.sleep(5)  # Можно заменить на WebDriverWait для более точного ожидания

# Парсинг данных
products = []

try:
    # Получение списка товаров
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "subcategory-or-type__products"))
    )

    for item in items:

        try:
            # Название товара
            name = item.find_element(By.CLASS_NAME, "product-card-name").text
            title = name.get_attribute("title")
            try:
                id = item.find_element(By.CLASS_NAME, "catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop").text
            except:
                id = "idinahyi"
            # Цены
            try:
                price_with_discount = item.find_element(By.CLASS_NAME, "product-price__sum-rubles").text
            except:
                price_with_discount = "Нет скидки"

            try:
                price_without_discount = item.find_element(By.CLASS_NAME, "product-unit-prices__old-wrapper").text
            except:
                price_without_discount = "Нет старой цены"

            # Бренд
            try:
                brand = item.find_element(By.CLASS_NAME, "product-card__brand").text
            except:
                brand = "Не указано"

            # Ссылка на товар
            link = item.find_element(By.CLASS_NAME, "catalog-2-level-product-card__middle").get_attribute("href")

            # Добавление данных о товаре в список
            products.append({
                "name": name,
                "id": id,
                "price_with_discount": price_with_discount,
                "price_without_discount": price_without_discount,
                "brand": brand,
                "url": link
            })
        except Exception as e:
            print(f"Ошибка при обработке товара: {e}")

finally:
    # Закрытие браузера
    driver.quit()

# Сохранение данных в JSON
output_file = "metro_coffee.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"Данные успешно сохранены в {output_file}")


#id товара из сайта/приложения,  наименование, ссылка на товар, регулярная цена, промо цена,

#бренд