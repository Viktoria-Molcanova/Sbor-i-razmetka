import requests
import json
import logging
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s %(message)s")

city = "Krasnoyarsk"
valid_categories = ['coffee shops', 'museums', 'parks', 'zoo', 'cafe', 'park', 'shops', 'restaurants']

print("Выберите категорию из следующего списка:")
for index, category in enumerate(valid_categories, start=1):
    print(f"{index}. {category}")

choice = int(input("Введите номер категории: ")) - 1

while choice < 0 or choice >= len(valid_categories):
    print("Неверный выбор, попробуйте снова.")
    choice = int(input("Введите номер категории: ")) - 1

category = valid_categories[choice]

url = "https://api.foursquare.com/v3/places/search"

params = {
    "limit": 10,
    "client_id": os.getenv("client_id"),
    "client_secret": os.getenv("client_secret"),
    "near": city,
    "query": category,
    "fields": "name,location,rating"
}

headers = {
    "Accept": "application/json",
    "Authorization": os.getenv("Authorization")
}

response = requests.get(url=url, params=params, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        try:
            print("Название:", venue["name"])
            print("Адрес:", venue["location"]["address"] if 'address' in venue["location"] else "Адрес не найден.")
            print("Рейтинг:", venue["rating"] if 'rating' in venue else "Рейтинг не найден.")
            print("\n")
        except KeyError as e:
            logging.error(f"Отсутствует поле : {e}")

    logging.info(f"Статус запроса: {response.status_code}")
else:
    print("Ошибка, код:", response.status_code)
