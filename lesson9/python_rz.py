from requests import get
from bs4 import BeautifulSoup
from sys import argv

from_, to, date = argv[1:]
date = date.replace(".", "-")

params = {"from": from_, "to": to, "date": date}

# ДАТА: ГОД.МЕСЯЦ.ДЕНЬ

response = get("https://pass.rw.by/ru/route/?", params=params)

if response.status_code != 200:
    raise Exception("Response.status_code != 200")

soup = BeautifulSoup(response.content, "lxml")
rows_div = soup.select_one("#sch-route > div.col-md-9.col-xs-12")

for row in rows_div.select(".sch-table__row-wrap"):
    train = row.select_one(".train-route")
    departure_time = row.select_one(".departure > .train-from-time")
    arrival_time = row.select_one(".arrival > .train-to-time")
    seats = row.select_one(".sch-table__tickets").text.split()

    if len(seats) == 2:
        seats_text = f"Цена за место: {' '.join(seats)}"
    else:
        seats_text = f"Место, количество мест, цена: {' '.join(seats)}"



    print(f"""
    Поезд: {train.text}
    Отправление: {departure_time.text}
    Прибытие: {arrival_time.text.strip()}
    {seats_text}
    """)


