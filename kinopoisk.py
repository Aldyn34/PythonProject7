import requests
import json
import csv
from bs4 import BeautifulSoup


class LetterboxdParser:
    def __init__(self, base_url="https://letterboxd.com/moviedan1256/"):
        self.base_url = base_url
        self.films = []

    def fetch_films_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(self.base_url, headers=headers)

        if response.status_code != 200:
            print("Ошибка загрузки страницы", response.status_code)
            return ""

        return response.text

    def parse_films_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        films = []

        for film in soup.find_all('li', class_='listitem poster-container'):
            title_tag = film.find('img', alt=True)
            rating_tag = film.find('span', class_='average-rating')
            year_tag = film.find('span', class_='year')

            if title_tag and rating_tag and year_tag:
                title = title_tag['alt']
                rating = float(rating_tag.text.strip())
                year = int(year_tag.text.strip())

                if year >= 1999:  # Ограничение по последним 25 годам
                    films.append({'title': title, 'rating': rating, 'year': year})

        films.sort(key=lambda x: x['rating'], reverse=True)
        return films[:10]  # Берём топ-10 фильмов

    def save_to_json(self, data, filename='top_letterboxd_films.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_to_csv(self, data, filename='top_letterboxd_films.csv'):
        if not data:
            print("Нет данных для сохранения.")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "rating", "year"])
            writer.writeheader()
            writer.writerows(data)

    def run(self):
        html = self.fetch_films_data()
        if not html:
            print("Не удалось получить данные о фильмах.")
            return

        films = self.parse_films_data(html)

        if not films:
            print("Не найдено популярных фильмов за последние 25 лет.")
            return

        self.films = films
        self.save_to_json(films)
        self.save_to_csv(films)
        print(f"Проанализировано {len(films)} популярных фильмов.")


if __name__ == "__main__":
    parser = LetterboxdParser()
    parser.run()
