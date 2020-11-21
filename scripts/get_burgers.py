import re
from typing import List

import requests
from bs4 import BeautifulSoup


class Burger:
    def __init__(self, name: str, explanation: str = "", additional_information: str = "") -> None:
        super().__init__()
        self.name = name
        self.explanation = explanation
        self.additional_information = additional_information


class Episode:
    def __init__(self, number: int, name: str, burgers=None) -> None:
        super().__init__()
        self.number = number
        self.name = name
        self.burgers = burgers if burgers else []


class Season:
    def __init__(self, number: int, episodes: List[Episode] = None) -> None:
        super().__init__()
        self.number = number
        self.episodes = episodes if episodes else []


def get_html(url: str) -> str:
    response = requests.get(url)

    if 200 <= response.status_code < 300:
        return response.text

    raise requests.HTTPError(response.reason)


def get_season_episodes(soup):
    season_episodes = {}
    for season in [heading for heading in (soup.find("div", "mw-parser-output").find_all("h2", recursive=False)) if
                   re.match(r"Season \d+", heading.text)][:8]:
        episodes = []
        for episode in season.find_next_siblings("h3"):
            if episode.find_previous_sibling("h2") is not season:
                break
            episodes.append(episode)

        season_episodes[season] = episodes
    return season_episodes


def main():
    soup = BeautifulSoup(get_html("https://bobs-burgers.fandom.com/wiki/Burger_of_the_Day"), 'lxml')
    season_episodes = get_season_episodes(soup)
    print(season_episodes)


if __name__ == "__main__":
    main()
