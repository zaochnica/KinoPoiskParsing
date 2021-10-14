from collections import Counter
from time import sleep

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference


def parse():
    data = []

    for page in range(1, 6):
        print('Page=', page)
        url = f"https://www.kinopoisk.ru/lists/series-top250/?page={page}&tab=all"
        r = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(r.text, 'lxml')

        films = soup.findAll('div', class_='desktop-rating-selection-film-item')
        for film in films:
            film_type = film.find(
                'div', class_='selection-film-item-meta selection-film-item-meta_theme_desktop'
            ).find(
                'a', class_='selection-film-item-meta__link'
            ).findAll('span', class_='selection-film-item-meta__meta-additional-item')[1].text
            data.extend([i.strip() for i in film_type.split(",")])

    return Counter(data)


def write_chart(genres: Counter):
    wb = Workbook()
    ws = wb.active

    for genre, number in genres.items():
        ws.append([genre, number])

    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Статистика жанров"
    values = Reference(ws, min_col=2, max_col=2, min_row=1, max_row=len(genres))
    labels = Reference(ws, min_col=1, max_col=1, min_row=1, max_row=len(genres))
    chart.add_data(values)
    chart.set_categories(labels)
    ws.add_chart(chart, "C1")

    wb.save("Genres.xlsx")


def main():
    genres = parse()
    write_chart(genres)


if __name__ == '__main__':
    main()
