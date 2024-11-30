from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time




options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# URL
url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search"
driver.get(url)

# ЗАГРУЗКА САЙТА #
time.sleep(5)

# Счётчик добавлен для быстрой работы скрипта
a = 0
products = []
while a < 7:
    wait = WebDriverWait(driver, 1)
    load_more_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div/div/div[3]/div[1]/main/div[2]/button")))
    load_more_button.click()
    time.sleep(5)
    a += 1
# Подсчёт количества товаров
product_elements = driver.find_elements(By.CLASS_NAME, "catalog-2-level-product-card")
print(f"Найдено карточек товаров: {len(product_elements)}")

for element in product_elements:
    try:
        # Название товара
        name = element.find_element(By.CLASS_NAME, "product-card-name__text").text
        # Цены
        try:
            price_with_discount = element.find_element(By.CLASS_NAME, "product-price__sum-rubles").text
        except:
            price_with_discount = "Нет скидки"
        try:
            price_without_discount = element.find_element(By.CLASS_NAME, "product-unit-prices__old-wrapper").text
        except:
            price_without_discount = "Нет старой цены"
        # Бренд| нет блока с брендом товара #
        try:
            brand = name[:18]
        except:
            brand = "Не указано"
        try:
            id = element.get_attribute("id")
        except:
            id = "Ошибка"

        # Ссылка на товар
        try:
            link = element.find_element(By.CLASS_NAME, "product-card-name")
            link2 = link.get_attribute("href")
        except:
            link2 = "нет ссылки"
        # Добавление данных о товаре в список
        products.append({
            "name": name,
            "id": id,
            "price_with_discount": price_with_discount,
            "price_without_discount": price_without_discount,
            "brand": brand,
            "url": link2
        })
    except Exception as e:
        print(f"Ошибка при обработке товара: {e}")

driver.quit()

# ЗАПИСЬ #
output_file = "metro_coffee.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"Данные успешно сохранены в {output_file}")
