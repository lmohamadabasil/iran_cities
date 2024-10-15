import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://iraniju.ir/iran-city/"

response = requests.get(url)

if response.status_code == 200:
    print("صفحه با موفقیت دریافت شد")
else:
    print("خطا در دریافت صفحه:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

conn = sqlite3.connect("cities.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        province_id INTEGER,
        cityname TEXT
    )
""")

for province_id in range(1, 32): 
    selector = f"#the-post > div.entry-content.entry.clearfix > div.wp-block-columns.is-layout-flex.wp-container-core-columns-is-layout-{province_id}.wp-block-columns-is-layout-flex > div:nth-child(1) > ol > li"
    
    cities = soup.select(selector)
    
    if not cities:
        print(f" not found {province_id}")
    
    for city in cities:
        city_name = city.text.strip()
        
        print(f"province : {province_id} - city : {city_name}")
        
        cursor.execute(
            "INSERT INTO cities (province_id, cityname) VALUES (?, ?)",
            (province_id, city_name)
        )

conn.commit()

conn.close()

print("اطلاعات با موفقیت ذخیره شد.")
