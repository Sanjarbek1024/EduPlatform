import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

# Brauzer sozlamalari
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# WebDriver
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# Kategoriyalar
categories = {
    "Elektronika": "https://www.olx.uz/d/elektronika/",
    "Avtomobil": "https://www.olx.uz/d/transport/",
    "Kochmas mulk": "https://www.olx.uz/d/nedvizhimost/",
    "Uy-rozgor": "https://www.olx.uz/d/dom-i-sad/",
}

all_data = []

for category_name, base_url in categories.items():
    print(f"\n\n {category_name} kategoriyasi:")
    
    for page in range(1, 11):  # 1-dan 10-sahifagacha, Sahifalarni fix qilish
        url = f"{base_url}?page={page}"
        print(f"\n  🌐 Sahifa: {page} - {url}")

        driver.get(url)
        time.sleep(random.uniform(3, 6))  # Delay random

        soup = BeautifulSoup(driver.page_source, "html.parser")
        ads = soup.find_all('div', attrs={'data-testid': 'l-card'})

        if not ads:
            print("\n   ⚠️ E'lon topilmadi. Sahifa mavjud emas yoki yuklanmagan.")
            break

        for ad in ads:
            title_tag = ad.find('h6') or ad.find('h4')
            price_tag = ad.find('p', attrs={'data-testid': 'ad-price'})
            location_tag = ad.find('p', attrs={'data-testid': 'location-date'})
            link_tag = ad.find('a', href=True)

            title = title_tag.text.strip() if title_tag else "Nomalum"
            price = price_tag.text.strip() if price_tag else "Nomalum"
            location_text = location_tag.text.strip() if location_tag else "Nomalum"
            link = "https://www.olx.uz" + link_tag['href'] if link_tag else ""

            if " - " in location_text:
                location, date = location_text.split(" - ", 1)
            else:
                location, date = location_text, ""

            all_data.append([category_name, title, price, location, date, link])

# Brauzerni yopish
driver.quit()

# CSV faylga yozish
with open("olx_barcha_kategoriyalar.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Kategoriya", "Sarlavha", "Narx", "Joy", "Sana", "Link"])
    writer.writerows(all_data)

print("\n✅ Barcha malumotlar 'olx_barcha_kategoriyalar.csv' fayliga saqlandi.")