from grequests import get as gget, map as gmap
from requests import get
from bs4 import BeautifulSoup

response = get("https://iteen.by/programs/?utm_source=google&utm_medium=cpc&utm_campaign=search_brendovie&utm_content=665225498286&utm_term=iteen&utm_id=18464017614&gad_source=1&gclid=CjwKCAiA9ourBhAVEiwA3L5RFusvqcw0-AyTcHjHosuN2CHs0V_3KkBDg-NjSh5RjvRUB-bKJHPyuhoCakMQAvD_BwE")

if response.status_code != 200:
    raise Exception("Response.status_code != 200")

html = response.content
soup = BeautifulSoup(html, "lxml")

max_page = int(soup.select_one("#ajax_paging > li:nth-child(8) > a").text)
pages_requests = [gget(f"https://iteen.by/programs?&PAGEN_1={page_number}") for page_number in range(1, max_page+1)]
pages_responses = gmap(pages_requests)

for page in pages_responses:
    html = page.content
    soup = BeautifulSoup(html, "lxml")

    programs_div = soup.select(".prog-list-2__item")

    for program in programs_div:
        title = program.select_one(".prog-item-2__m-title").text
        class_ = program.select_one(".prog-item-2__tag").text
        price = program.select_one(".prog-item-2__price").text

        print(f"{class_+':':<30} {title.upper():<40} {price}")






