import requests
from bs4 import BeautifulSoup
import json

# Функция для получения списка всех категорий книг
def get_categories():
    try:
        url = "https://books.toscrape.com/index.html"
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = soup.select("ul.nav-list li")
        category_links = {}
        for category in categories:
            link = category.a['href']
            name = category.a.string.strip() if category.a and category.a.string else 'Неизвестная категория'
            category_links[name] = link
        return category_links
    except requests.RequestException as e:
        print(f"Ошибка при получении категорий: {e}")
        return {}

# Функция для скрапинга книг из заданной категории
def scrape_books_from_category(category_url):
    books = []
    base_url = "https://books.toscrape.com"

    while True:
        try:
            response = requests.get(category_url)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            book_items = soup.find_all(class_='product_pod')

            for book in book_items:
                title = book.h3.a['title'] if book.h3 and book.h3.a else 'Без названия'
                price_text = book.find(class_='price_color').text
                price = float(price_text[1:]) if price_text.startswith('£') else 0.0
                stock_text = book.find(class_='instock availability').text.strip()
                stock = int(stock_text.split()[2]) if 'in stock' in stock_text else 0
              
                # Получение ссылки на страницу книги для извлечения описания
                book_link = book.h3.a['href']
                book_response = requests.get(f"{base_url}{book_link}")
                book_response.raise_for_status() 
                book_soup = BeautifulSoup(book_response.text, 'html.parser')
                description = book_soup.find(id='product_description')
                description = description.find_next_sibling('p').text if description else 'Описание недоступно'

                books.append({
                    'title': title,
                    'price': price,
                    'stock': stock,
                    'description': description
                })

            # Проверка наличия следующей страницы
            next_button = soup.find(class_='next')
            if next_button:
                next_link = next_button.a['href']
                category_url = f"{base_url}/catalogue/category/books/{next_link}"
            else:
                break
        except requests.RequestException as e:
            print(f"Ошибка при скрапинге категории: {e}")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            break

    return books

# Основная функция
def main():
    all_books = []
    categories = get_categories()
    for category_name, category_link in categories.items():
        print(f"Скрапинг категории: {category_name}")
        full_category_url = f"https://books.toscrape.com/{category_link}"

        books = scrape_books_from_category(full_category_url)
        all_books.extend(books)

    # Сохранение данных в JSON файл
    try:
        with open('books_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(all_books, json_file, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены в файл books_data.json")
    except IOError as e:
        print(f"Ошибка при сохранении данных в файл: {e}")

if __name__ == "__main__":
    main()
