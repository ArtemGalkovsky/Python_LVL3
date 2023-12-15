from grequests import get as gget, map as gmap, AsyncRequest
from requests import Response, get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from proxy_cheker import check_with_printing
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from db import DB

ua = UserAgent()


class CookParser:
    DISHES_URL = "http://www.tvcook.ru/{category}/page/{page}"
    CATEGORIES_URL = "http://www.tvcook.ru/katalog-retseptov"
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9,en-US;q=0.8,ru-RU;q=0.7,be;q=0.6',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random
    }

    def __init__(self, proxies: list[str]) -> None:
        self.driver: webdriver.Chrome = webdriver.Chrome(service=ChromeService())
        self.categories: dict[str: str] = self.get_categories()
        self.proxies: list[str] = proxies

    def get_categories(self) -> dict[str: str]:
        self.driver.get(self.CATEGORIES_URL)
        sleep(1)

        print(f"[{__name__}](CookParser)(get_categories) START GETTING!")
        categories_elements = self.driver.find_elements(By.CSS_SELECTOR, ".entry-content li > a")

        categories = {}
        for category_element in categories_elements:
            url = category_element.get_attribute("href").replace("https://www.tvcook.ru/", "")
            name = category_element.text

            categories[name] = url

        categories["Главная страница"] = ""
        print(f"[{__name__}](CookParser)(get_categories) END! Categories are", categories)
        return categories

    def retry_request(self, request: AsyncRequest) -> Response | str | None:
        print(f"[{__name__}](CookParser)(retry_request) Can't reach", request.url)
        try:
            try_response = get(request.url, headers=self.HEADERS, timeout=10)
            print(f"[{__name__}](CookParser)(retry_request) Try response is",
                  try_response)

            if isinstance(try_response, Response):
                if try_response.status_code == 200:
                    print(f"[{__name__}](CookParser)(retry_request) REACHED!")
                    return try_response
                elif try_response.status_code == 404:
                    print(f"[{__name__}](CookParser)(retry_request) FINAL PAGE, 404!")
                return try_response
        except Exception as e:
            print(f"[{__name__}](CookParser)(retry_request) Not reached!", e)

    @staticmethod
    def send_requests(requests: list[AsyncRequest]) -> list[AsyncRequest | Response]:
        """
        Makes requests and check if request is success
        If not success - replaces response with it's request
        :param requests: list[AsyncRequest]
        :return: list[AsyncRequest | Response]
        """
        for request in requests:
            request.headers = {"user-agent": ua.random}

        responses = gmap(requests, size=21)
        print(f"[{__name__}](CookParser)(send_requests) Urls are", [request.url for request in requests])

        print(f"[{__name__}](CookParser)(send_requests) Responses are", responses)
        for index, response in enumerate(responses):
            if not response or response.status_code != 200:
                responses[index] = requests[index]

        print(f"[{__name__}](CookParser)(send_requests) Now responses are", responses)
        return responses

    def send_requests_with_validation(self, requests: list[AsyncRequest]) -> list[AsyncRequest | Response | str]:
        all_responses = []
        bad_requests = {}
        while requests:
            responses = self.send_requests(requests)

            requests = []
            for response in responses:
                if isinstance(response, AsyncRequest):
                    response.proxies = {"http": choice(self.proxies)}
                    requests.append(response)

                    if response.url not in bad_requests:
                        bad_requests[response.url] = 1
                    else:
                        bad_requests[response.url] += 1

                    if bad_requests[response.url] >= 3:
                        retry_result = self.retry_request(response)

                        if not retry_result:
                            return []

                        all_responses.append(retry_result)
                        bad_requests[response.url] = 0
                        requests.remove(response)
                else:
                    all_responses.append(response)
                    if response in bad_requests:
                        bad_requests[response.url] = 0

        return all_responses

    @staticmethod
    def parse_recipe(soup: BeautifulSoup) -> dict[str: str]:
        dish_ingredients = soup.select('[itemprop="recipeIngredient"]')

        recipe = {}
        for ingredient in dish_ingredients:
            try:
                name = ingredient.select_one('.ingredients__name').text.strip()
                count = ingredient.text.replace(name, "").replace(" ", " ").strip()

                recipe[name] = count
            except Exception as e:
                print(f"[{__name__}](CookParser)(parse_recipe) Incorrect ingredient format! Parsing pattern #2!...")

                name_and_count = ingredient.text.split("—")

                if len(name_and_count) == 2:
                    name = name_and_count[0].strip()
                    count = name_and_count[1].strip()

                    recipe[name] = count
                else:
                    recipe[name_and_count[0]] = "?"

        return recipe

    @staticmethod
    def parse_steps(soup: BeautifulSoup) -> dict[int: str]:
        dish_cooking_steps = soup.select(".recipe-steps > li")

        steps = {}
        for index, step in enumerate(dish_cooking_steps, 1):
            steps[index] = step.text.strip()

        return steps

    @staticmethod
    def parse_dish_info(soup: BeautifulSoup) -> dict[str: str, str: str, str: str, str: str]:
        try:
            dish_category_href = soup.select_one('head > [rel="canonical"]').attrs.get("href")
        except:
            dish_category_href = soup.select_one('head > [rel="alternate"]').attrs.get("href")

        dish_category_href = dish_category_href.replace("https://www.tvcook.ru/recipes/", "")
        dish_category_split = dish_category_href.split("/")[:-1]
        dish_category = "/".join(dish_category_split)

        dish_id = soup.select_one("article").attrs.get("id")
        dish_name = soup.select_one(".entry-title").text

        try:
            dish_description = soup.select_one("div.entry-content > p").text.strip()
        except:
            dish_description = soup.select_one("div.entry-content").text.strip()

        return {"category": dish_category, "id": dish_id, "name": dish_name, "description": dish_description}

    def parse_pages(self, pages: list[str]) -> \
            list[dict[str: str, str: str, str: str, str: str, str: dict[str: str], str: dict[int, str]]]:
        dishes = []
        for page in pages:
            soup = BeautifulSoup(page, "lxml")

            with open("card.html", "w+", encoding="UTF-8") as fl:
                fl.write(page)

            dish_info = self.parse_dish_info(soup)

            print(f"[{__name__}](CookParser)(parse_pages) Parsing:", dish_info["name"],
                  dish_info["id"], dish_info["description"])

            dish_info["recipe"] = self.parse_recipe(soup)
            dish_info["steps"] = self.parse_steps(soup)

            dishes.append(dish_info)

        return dishes

    def parse_dishes_cards(self, dishes_urls: list[str]) -> \
            list[dict[str: str, str: str, str: str, str: str, str: dict[str: str], str: dict[int, str]]]:
        requests = [
            gget(
                href, headers=self.HEADERS, proxies={"http": choice(self.proxies)}, timeout=5
            )
            for href in dishes_urls]

        all_responses = self.send_requests_with_validation(requests)

        print(f"[{__name__}](CookParser)(get_dishes) All responses are good")

        all_dishes = self.parse_pages([response.text for response in all_responses])

        return all_dishes

    def parse_category(self, category: str, db_object: DB | None = None) -> \
            list[list[dict[str: str, str: str, str: str, str: str, str: dict[str: str], str: dict[int, str]]]]:
        category_path = self.categories[category]
        all_dishes = []

        page = 1
        while True:
            self.driver.get(self.DISHES_URL.format(category=category_path, page=page))

            try:
                self.driver.find_element(By.CSS_SELECTOR, ".error-404")
                print(f"[{__name__}](CookParser)(parse_category) Previous page was the last!")
                break
            except:
                print(f"[{__name__}](CookParser)(parse_category) This page is not the last")

            dishes_urls = []
            for dish_element in self.driver.find_elements(By.CSS_SELECTOR, ".content-card .content-card__title > a"):
                dishes_urls.append(dish_element.get_attribute("href"))

            current_dishes = self.parse_dishes_cards(dishes_urls)
            all_dishes.append(current_dishes)

            if db_object:
                db_object.add_all_dishes([current_dishes])

            page += 1
            sleep(5)

        return all_dishes

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    with open("proxies.txt") as fl:
        proxies = fl.read().splitlines()

    good_proxies = check_with_printing(proxies)

    parser = CookParser(good_proxies)
    db = DB("cooking.db")

    for category in parser.categories:
        if "/" in parser.categories[category]:
            continue
        print("Parsing", category)
        all_dishes = parser.parse_category(category, db_object=db)

    db.db2xlsx()
    print("END!!!!")
    exit(0)
