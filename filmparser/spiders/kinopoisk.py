import scrapy
from scrapy.http import HtmlResponse
import json

class KinopoiskSpider(scrapy.Spider):
    name = "kinopoisk"
    allowed_domains = ["kinorium.com"]
    start_urls = ["https://ru.kinorium.com/movies/cinema/"]

    def __init__(self, *args, **kwargs):
        super(KinopoiskSpider, self).__init__(*args, **kwargs)
        self.movies_data = []  # Список для хранения данных о фильмах

    def parse(self, response: HtmlResponse):
        try:
            movies = response.xpath("//div[contains(@class, 'movie')]")
            for movie in movies:
                title = movie.xpath(".//span[contains(@class,'title')]/text()").get()
                rating = movie.xpath(".//span[contains(@class,'rating')]/text()").get()
                if title and rating:  # Проверка наличия данных
                    self.movies_data.append({'title': title.strip(), 'rating': rating.strip()})  # Удаление лишних пробелов

            next_page = response.xpath("//a[@class='next']/@href").get()
            if next_page:
                yield response.follow(next_page, self.parse)
        except Exception as e:
            self.logger.error(f"Ошибка при парсинге страницы: {e}")

    def close(self, reason):
        try:
            with open('movies.json', 'w', encoding='utf-8') as f:
                json.dump(self.movies_data, f, ensure_ascii=False, indent=4)  # Сохранение всех данных
        except IOError as e:
            self.logger.error(f"Ошибка при записи в файл: {e}")