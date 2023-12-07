from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class Parser:
    SCROLL_PAUSE_TIME_SECONDS = 2
    MAIN_PAGE_URL = "https://robofinist.ru/event"
    COMPETITION_NOMINATIONS_PAGE = "https://robofinist.ru/event/info/competitions/id/{competition_id}"

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        self.driver.get(self.MAIN_PAGE_URL)

    def scroll_until_end(self):
        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(self.SCROLL_PAUSE_TIME_SECONDS)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @staticmethod
    def check_if_registration_ends(competition: WebElement) -> tuple[bool, str]:
        is_registration_closed_tag = competition.find_element(By.CSS_SELECTOR,
                                                              "div:nth-child(5) > div > p")
        if is_registration_closed_tag.text == "Регистрация завершена":
            return True, is_registration_closed_tag.text

        return False, is_registration_closed_tag.text.strip()

    @staticmethod
    def get_competition_id(competition: WebElement):
        event_url = competition.find_element(By.TAG_NAME, "a").get_attribute("href")
        return event_url[-event_url[::-1].index("/"):]

    def get_competitions_info(self) -> list[dict]:
        competitions = []
        for competition in self.driver.find_elements(By.CSS_SELECTOR,
                                                     "#root > div > div > div > div > div > div:nth-child(2) > div.col-xs-12.col-md-8.col-lg-9 > div > div > div > div"):

            if competition.text.strip():
                is_registration_ends, registration_text = self.check_if_registration_ends(competition)

                if is_registration_ends:
                    continue

                competition_id = self.get_competition_id(competition)

                competitions.append({"id": competition_id, "title": competition.text.strip(),
                                     "registration": registration_text})

        return competitions

    def get_kind(self, competition_id: int) -> str:
        self.driver.get(self.COMPETITION_NOMINATIONS_PAGE.format(competition_id=competition_id))

        try:
            button = self.driver.find_element(By.CSS_SELECTOR, "#more-programs-btn")
        except:
            return ""

        button.click()
        return self.driver.find_element(By.CSS_SELECTOR, ".kinds").text

    @staticmethod
    def check_if_nominations_in_kind(kind: str):
        for nomination in ("Roborace. Образовательные конструкторы. Junior",
                           "Roborace. Образовательные конструкторы",
                           "Roborace. PRO Mini",
                           "Следование по линии. Образовательные конструкторы",
                           "Большое путешествие младшая категория: образовательные конструкторы",
                           "RoboCupJunior Rescue Line",
                           "Эстафета",
                           "Футбол управляемых роботов 3x3",
                           "Футбол управляемых роботов 4x4",
                           "Интеллектуальное сумо 15х15: образовательные конструкторы",
                           "Кубок РТК. Искатель",
                           "Кубок РТК. Экстремал",
                           "FIRA Challenge - Autonomous Cars"):

            if nomination in kind:
                return True

        return False

    def get_competitions_with_valid_nominations(self, competitions: list[dict]) -> list[str]:
        valid_competitions = []
        for competition_dict in competitions:
            competition_id = competition_dict["id"]
            competition_title = competition_dict["title"]
            registration = competition_dict["registration"]

            kind = self.get_kind(competition_id)

            print(f"https://robofinist.ru/event/{competition_id}:\n"
                  f"{competition_title}\n\nНоминации:\n"
                  f"{kind}\n"
                  f"{registration}\n"
                  f"----------------------")

            if self.check_if_nominations_in_kind(kind):
                valid_competitions.append(f"https://robofinist.ru/event/{competition_id}:\n"
                                          f"{competition_title}\nНоминации:\n"
                                          f"{kind}\n"
                                          f"{registration}")

        return valid_competitions


if __name__ == "__main__":
    parser = Parser()
    parser.scroll_until_end()
    competitions_info = parser.get_competitions_info()
    valid_competitions = parser.get_competitions_with_valid_nominations(competitions_info)

    print("ПОДХОДЯЩИЕ:")
    print("\n----------------------\n".join(valid_competitions))
