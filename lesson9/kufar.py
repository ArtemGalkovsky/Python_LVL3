from grequests import get as gget, map as gmap
from requests import get
from bs4 import BeautifulSoup
from json import loads, dump
from openpyxl import Workbook
from time import sleep


def parse_many(tokens_list, pages):
    tokes_list2 = []
    ads_list = []

    for token_dict in tokens_list:
        print(token_dict)
        token = token_dict["token"]
        page = token_dict["num"]

        if page in pages:
            continue

        cursor_url = f"https://www.kufar.by/l/r~minsk/noutbuki?cursor={token}"
        url_for_be = get_url_for_be(cursor_url)

        tokens, ads = get_tokens_and_ads(url_for_be)
        tokes_list2.extend(tokens)
        ads_list.extend(ads)

        pages.append(page)
    return tokes_list2, ads_list


def parse() -> None:
    wb = Workbook()
    wb.create_sheet("notebooks")

    page_wb = wb.active

    notebooks_start_page = "https://www.kufar.by/l/r~minsk/noutbuki"
    url_for_be = get_url_for_be(notebooks_start_page)
    tokens_list, ads = get_tokens_and_ads(url_for_be)

    pages = []
    while len(tokens_list):
        tokens_list, ads = parse_many(tokens_list, pages=pages)
        print(pages, len(ads))

        for ad in ads:
            write_notebook_data(ad["ad_link"], page_wb)
            sleep(0.1)

        wb.save("notebooks_data.xlsx")


def get_url_for_be(url_with_cursor: str) -> str:
    response = get(url_with_cursor)

    if response.status_code != 200:
        raise Exception("get_url_for_be: Response.status_code != 200")

    soup = BeautifulSoup(response.content, "lxml")
    script_next_data = soup.select_one("#__NEXT_DATA__")
    json_data = loads(script_next_data.text)
    url_for_be = json_data["props"]["initialState"]["router"]["urlForBe"]

    return url_for_be


def get_tokens_and_ads(url_for_be: str) -> tuple:
    response = get(url_for_be)

    if response.status_code != 200:
        raise Exception("get_next_page_url_and_ads: Response.status_code != 200")

    json_data = loads(response.text)
    return json_data["pagination"]["pages"], json_data["ads"]


def write_notebook_data(url, page_wb):
    print("parsing", url)
    response = get(url)
    soup_page = BeautifulSoup(response.content, "lxml")

    url = response.url
    name_and_price = soup_page.select_one("title").text
    name_and_price_split = name_and_price.split()
    print(name_and_price_split)
    price_start_index = name_and_price_split.index("цена")
    try:
        price_end_index = name_and_price_split.index("р.", price_start_index)
    except:
        price_end_index = price_start_index + 2

    price = ''.join(name_and_price_split[price_start_index + 1:price_end_index])
    name = " ".join(name_and_price_split)[:price_start_index]

    page_wb.append((name, price, url))


parse()
