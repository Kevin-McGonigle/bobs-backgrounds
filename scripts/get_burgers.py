import re
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pandas import DataFrame


class Burger:
    def __init__(self, name: str, explanation: str = None, additional_information: str = None) -> None:
        super().__init__()
        self.name = name
        self.explanation = explanation
        self.additional_information = additional_information


class Episode:
    def __init__(self, number: int, name: str, burgers: List[Burger] = None) -> None:
        super().__init__()
        self.number = number
        self.name = name
        self.burgers = burgers if burgers else []


class Season:
    def __init__(self, number: int, episodes: List[Episode] = None) -> None:
        super().__init__()
        self.number = number
        self.episodes = episodes if episodes else []


def get_html(url: str = "https://bobs-burgers.fandom.com/wiki/Burger_of_the_Day") -> str:
    """
    Get HTML from the specified URL.

    :param url: The URL to get HTML from.
    :return: The retrieved HTML as a string.
    """
    response = requests.get(url)

    if 200 <= response.status_code < 300:
        return response.text

    raise requests.HTTPError(response.reason)


def get_burger(tag: Tag, season_number: int) -> Optional[Burger]:
    """
    Parse burger information from HTML.

    :param tag: The HTML tag to parse.
    :param season_number: The season that the burger appears in.
    :return: The parsed burger information.
    """
    if season_number < 9:
        try:
            title = tag.find(text=True, recursive=False).strip().split(" - ")
            name = title[0]
            explanation = title[1] if len(title) > 1 else None

            additional_information_list = tag.find("ul", recursive=False)
            additional_information = ". ".join([list_item.text.strip(" \n.") for list_item in
                                                additional_information_list.find_all("li",
                                                                                     recursive=False)]
                                               if additional_information_list else []) + "."
            return Burger(name, explanation, additional_information)
        except Exception:
            return None
    else:
        # TODO: Implement for season >= 9.
        return Burger("Placeholder")


def get_episode(tag: Tag, episode_number: int, season_number: int) -> Episode:
    """
    Parse episode information from HTML.

    :param tag: The HTML tag to parse.
    :param episode_number: The episode number.
    :param season_number: The season that the episode appears in.
    :return: The parsed episode information.
    """
    burgers = []
    if season_number < 9:
        episode_name = tag.text.strip()
        burgers_lists = tag.find_next_siblings("ul")
        for burgers_list in burgers_lists:
            if burgers_list:
                if burgers_list.find_previous_sibling("h3") is not tag:
                    break
                burgers.extend([burger for burger in
                                [get_burger(list_item, season_number) for list_item in
                                 burgers_list.find_all("li", recursive=False)] if burger is not None])
    else:
        episode_name = tag.find("td").text.strip("\" \n")
        burgers = [get_burger(tag, season_number)]
        for tr in tag.find_next_siblings("tr"):
            if len(tr.find_all("td")) == 3:
                break
            burgers.append(get_burger(tr, season_number))

    return Episode(episode_number, episode_name, burgers)


def get_season(tag: Tag) -> Season:
    """
    Parse season information from HTML.

    :param tag: The HTML tag to parse.
    :return: The parsed season information.
    """
    season_number = int(tag.text.strip().split()[-1])
    episodes = []

    if season_number < 9:
        for episode_number, heading in enumerate(tag.find_next_siblings("h3"), 1):
            if heading.find_previous_sibling("h2") is not tag:
                break
            episodes.append(get_episode(heading, episode_number, season_number))
    else:
        episode_number = 1
        for tr in tag.find_next_sibling("table").find_all("tr")[1:]:
            if len(tr.find_all("td")) == 3:
                episode_number += 1
                episodes.append(get_episode(tr, episode_number, season_number))

    return Season(season_number, episodes)


def get_seasons(soup: BeautifulSoup) -> List[Season]:
    """
    Parse seasons from HTML.

    :param soup: The soup to parse seasons from.
    :return: A list of parsed seasons information.
    """
    return [get_season(heading) for heading in (soup.find("div", "mw-parser-output").find_all("h2", recursive=False)) if
            re.match(r"Season \d+", heading.text)]


def pretty_print_seasons(seasons: List[Season] = None) -> None:
    """
    Pretty print a list of seasons.

    :param seasons: The seasons to pretty print.
    """
    if not seasons:
        return

    for season in seasons:
        print(f"Season {season.number}")
        for episode in season.episodes:
            print(f"  Episode {episode.number}: {episode.name}")
            for burger in episode.burgers:
                print(f"    Burger: {burger.name}")
                if burger.explanation:
                    print(f"      Explanation: {burger.explanation}")
                if burger.additional_information:
                    print(f"      Additional Information: {burger.additional_information}")
            print()
        print()


def save_as_excel(seasons: List[Season] = None) -> None:
    """
    Save information in a list of seasons as an excel spreadsheet.

    :param seasons: The seasons to save.
    """
    if not seasons:
        return

    episode_data = []
    burger_data = []
    for season in seasons:
        for episode in season.episodes:
            episode_data.append((episode.name, season.number, episode.number))
            for burger in episode.burgers:
                burger_data.append(
                    (burger.name, burger.explanation, season.number, episode.number, burger.additional_information))

    path = Path("output/spreadsheets")
    path.mkdir(parents=True, exist_ok=True)

    DataFrame(data=episode_data, columns=["name", "season", "number"]).to_excel(f"{path}/episodes.xlsx", index=False)
    DataFrame(data=burger_data,
              columns=["name", "explanation", "season_number", "episode_number", "additional_information"]).to_excel(
        f"{path}/burgers.xlsx", index=False)


def main() -> None:
    """
    The main function.
    """
    soup: BeautifulSoup = BeautifulSoup(get_html(), 'lxml')
    seasons = get_seasons(soup)
    pretty_print_seasons(seasons)
    save_as_excel(seasons)


if __name__ == "__main__":
    main()
