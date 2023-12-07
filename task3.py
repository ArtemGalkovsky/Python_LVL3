from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
from win32api import MessageBox


def str2float(string: str) -> float:
    if string:
        return float("".join(symbol for symbol in string if symbol.isdigit() or symbol == "."))
    return 0


def parse(from_: str, to: str, date: str, passengers_count: str, time_from: str, time_to: str) -> None:
    driver.get(
        f"https://atlasbus.by/Маршруты/{from_.strip()}/{to.strip()}?date={date.strip()}&passengers={passengers_count.strip()}")
    div_container = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[3]/div')

    for index, div in enumerate(div_container, 1):
        seats = str2float(div.find_element(By.CSS_SELECTOR, "p").text)

        if seats >= int(passengers_count):
            time_start_datetime = datetime.strptime(div.find_element(By.CSS_SELECTOR, "div").text[:5].strip(), '%H:%M')

            time_from_datetime = datetime.strptime(time_from.strip(), '%H:%M')
            time_to_datetime = datetime.strptime(time_to.strip(), '%H:%M')

            print(f"#{index} Мест: {int(seats)}, Время отправления {time_start_datetime}, ваше желаемое время от "
                  f"{time_from_datetime}, до {time_to_datetime}")

            if time_from_datetime <= time_start_datetime <= time_to_datetime:
                print(f"НАЙДЕН! Маршрутка #{index} на сайте!")
                MessageBox(0, f'МАРШРУТКА НАЙДЕНА! НОМЕР #{index} на сайте', 'Маршрутка найдена!')
                return



if __name__ == "__main__":
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    from_, to, date, passengers_count, time_from, time_to = input("начальный город, конечный город, дата"
                                                                  " (xxxx-xx-xx), количество пассажиров, желаемое"
                                                                  " время от, желаемое время до > ").split(",")

    while 1:
        parse(from_, to, date, passengers_count, time_from, time_to)
        sleep(60)


