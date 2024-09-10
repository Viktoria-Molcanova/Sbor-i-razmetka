import pymongo
import json

# MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print("Успешно подключено к MongoDB")
except pymongo.errors.ConnectionError as e:
    print(f"Ошибка подключения к MongoDB: {e}")
    exit(1)

# Создание БД
database_name = "HW3"
database = client[database_name]

# Создание коллекции
collection_name = "books"
collection = database[collection_name]

# Загрузка данных из файла JSON
try:
    with open("books_data.json", encoding='utf-8') as file:
        data = json.load(file)
        print("Данные успешно загружены из файла JSON")
except FileNotFoundError:
    print("Ошибка: Файл books_data.json не найден.")
    exit(1)
except json.JSONDecodeError:
    print("Ошибка: Не удалось декодировать JSON.")
    exit(1)

# Вставка данных в коллекцию
try:
    collection.insert_many(data)
    print("Данные успешно вставлены в коллекцию")
except pymongo.errors.BulkWriteError as e:
    print(f"Ошибка при вставке данных: {e.details}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
    
# Получение всех документов из коллекции
try:
    all_books = collection.find()
    for book in all_books:
        print(book)
except Exception as e:
    print(f"Ошибка при выполнении запроса: {e}")
