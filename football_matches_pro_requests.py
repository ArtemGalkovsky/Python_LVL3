from requests import get, post
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from pygame import mixer
from pygame.mixer import Sound


class FootballParser:
    ALL_EVENTS_URL = "https://4score.ru/events/get/?date={date}&status=all"
    STATS_URL = "https://4score.ru/teams/{team_name}/stats/"

    def get_events(self) -> list[dict[str, str | int | bool]]:
        date = datetime.now().strftime("%Y-%m-%d")
        html = get(self.ALL_EVENTS_URL.format(date=date)).text

        soup = BeautifulSoup(html, "lxml")
        events_table = soup.select(".events-table-event-data")

        events = []
        for event in events_table:
            status = event.select_one(".events-table-event-status").text.strip()
            is_started = True if status else False
            url = "https://4score.ru" + event.select_one("a").attrs.get("href")

            print(f"PARSED: URL TO PARSE: {url:<100} : IS STARTED: {is_started:<10} : STATUS: {status}")

            events.append({"status": status, "is_started": is_started, "url": url})

        return events

    def get_valid_matches(self) -> list[dict[str, str | bool | int]]:
        events = self.get_events()

        valid_events = []
        for event in events:
            is_started = event["is_started"]
            status = event["status"]
            url = event["url"]

            if not is_started or status == "Отложено":
                valid_events.append({"is_started": is_started, "status": status, "url": url})

        return valid_events

    @staticmethod
    def get_team_names(url: str) -> list[str]:
        html = get(url).text

        soup = BeautifulSoup(html, "lxml")
        teams_urls = soup.select(".event-disclaimer-team > a")

        teams_names = []
        for team_url in teams_urls:
            team_url = team_url.attrs.get("href")
            team_name_start = team_url.find("/", 1) + 1

            teams_names.append(team_url[team_name_start:-1].strip())

        return teams_names

    def get_team_matches(self, team_name: str) -> list[dict[str, str | int]]:
        html = post(self.STATS_URL.format(team_name=team_name), data={"type": "goals"}).text

        soup = BeautifulSoup(html, "lxml")

        matches = []
        for match in soup.select("body > div > table.display > tbody > tr"):
            date = match.select_one("td:nth-child(2)").text
            league = match.select_one("td:nth-child(3)").text
            local_team_name = match.select_one("td:nth-child(4)").text
            local_team_goals = match.select_one("td:nth-child(5)").text
            visitor_team_goals = match.select_one("td:nth-child(6)").text
            visitor_team_name = match.select_one("td:nth-child(7)").text

            matches.append({
                "date": date,
                "league": league,
                "local_team_name": local_team_name,
                "local_team_goals": int(local_team_goals),
                "visitor_team_name": visitor_team_name,
                "visitor_team_goals": int(visitor_team_goals)
            })

        return matches

    @staticmethod
    def has_2_last_draws_matches(matches: list[dict[str, str | int]]) -> bool:
        if len(matches) < 2:
            print("NO MATCHES!")
            return False

        if matches[0]["local_team_goals"] == matches[0]["visitor_team_goals"] == 0 and \
                matches[1]["local_team_goals"] == matches[1]["visitor_team_goals"] == 0:
            print("CONFIRMED! 2 LAST MATCHES ARE DRAWS", matches[:2])
            return True

        print("NOT CONFIRMED. 2 LAST MATCHES ARE DRAWS", matches[:2])
        return False


def main(sound: Sound) -> None:
    parser = FootballParser()
    matches = parser.get_valid_matches()

    print_matches_of_these_teams = []
    for match in matches:
        team_names = parser.get_team_names(match["url"])

        print("MATCH TEAM NAMES:", *team_names)
        local_team_matches = parser.get_team_matches(team_names[0])
        if parser.has_2_last_draws_matches(local_team_matches):
            print_matches_of_these_teams.append(team_names[0])

        visitor_team_matches = parser.get_team_matches(team_names[1])
        if parser.has_2_last_draws_matches(visitor_team_matches):
            print_matches_of_these_teams.append(team_names[1])

        sleep(1)

    print("VALID TEAMS:", *print_matches_of_these_teams)

    for match in matches:
        for team in print_matches_of_these_teams:
            if team in match["url"]:
                print("VALID FEATURE MATCH:", match["url"], "TEAM WITH ZERO:ZERO PREVIOUS 2 RESULTS IS", team.upper())

                sound.play()


if __name__ == "__main__":
    mixer.init()
    sound = mixer.Sound("bell.wav")

    while True:
        main(sound)
        sleep(300)
