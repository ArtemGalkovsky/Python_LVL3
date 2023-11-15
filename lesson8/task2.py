from requests import get
from bs4 import BeautifulSoup


def get_forecast(split_forecast: list, full_forecast: str):
    forecast = []
    for index, data in enumerate(split_forecast, 1):
        forecast.append(data)

        if index % 5 == 0:
            full_forecast += f"""
{forecast[0]}:
Температура: {forecast[1]}:
{forecast[2]}: {forecast[3]}
Вероятность дождя: {forecast[4]}
"""
            forecast = []

    return full_forecast


response = get("https://www.meteoservice.ru/weather/overview/minsk")

if response.status_code != 200:
    raise Exception("Parsing failed.")

html = response.content

soup = BeautifulSoup(html, "lxml")
current = soup.select_one(
    'body > div.off-canvas-wrapper > div.off-canvas-content > div > div > div:nth-child(8) > div.small-12.large-9.columns > div:nth-child(1) > div.small-12.medium-4.large-4.columns.current-weather > div.callout.magnify-on-hover')
#   'body > div.off-canvas-wrapper > div.off-canvas-content > div > div > div:nth-child(8) > div.small-12.large-9.columns > div:nth-child(1) > div.small-12.medium-4.large-4.columns.current-weather > div.callout.magnify-on-hover'
current_split = current.text.split()

full_forecast = f"""
{current_split[0]} {current_split[1]} {current_split[2]}:
Температура: {current_split[6]}
{current_split[7]}: {current_split[8]}
{current_split[9]}: {current_split[10]} {current_split[11]}{current_split[12]}

Сегодня:
"""

with open("resp_weather.html", "wb") as fl:
    fl.write(html)

today_1 = soup.select_one(
    "body > div.off-canvas-wrapper > div.off-canvas-content > div > div > div:nth-child(8) > div.small-12.large-9.columns > div:nth-child(1) > div.small-12.medium-8.large-8.columns > div.row > div.column.today > div > div"
)
today_1_split = today_1.text.split()
full_forecast = get_forecast(today_1_split, full_forecast)

tomorrow = soup.select_one("body > div.off-canvas-wrapper > div.off-canvas-content > div > div.content.use-bg > div:nth-child(8) > div.small-12.large-9.columns > div:nth-child(1) > div.small-12.medium-8.large-8.columns > div.row > div.column.tomorrow")
tomorrow_split = tomorrow.text.split()

full_forecast += "\nЗавтра:\n"
full_forecast = get_forecast(tomorrow_split, full_forecast)

print(full_forecast)
