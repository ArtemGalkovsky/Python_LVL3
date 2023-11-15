from requests import get
from bs4 import BeautifulSoup


def get_page(page=1):
    url = "https://www.21vek.by/notebooks/page:{page}/?order%5Bpopularity%5D=desc&filter%5Bsa%5D=".format(page=page)
    response = get(url)

    if response.status_code != 200:
        raise Exception("Parsing failed.")

    return response

page_count = get_page()


page = 1
while 1:
    page_response = get_page(page)
    if len(page_response.history) > 0:
        break

    page_content = page_response.content
    soup = BeautifulSoup(page_content, "lxml")

    notebooks = soup.select("li.result__item")

    if not len(notebooks):
        break

    for notebook in notebooks:
        model = notebook.select_one(".result__name").text
        price_element = notebook.select_one(".g-item-data")
        if price_element is None:
            continue

        if page == 20:
            with open("resp.html", "wb") as fl:
                fl.write(page_content)

        price = price_element.text
        url = notebook.select_one("a").attrs.get("href")

        if len(model) > 70:
            model = model[:65] + "..."

        print(f"{page} стр. {model:<70} {price + 'р':<15} {url}")

    page += 1