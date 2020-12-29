# TODO: Populate tables.

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


def is_episode_tr(tr: Tag) -> bool:
    """
    Check if a table row for season 9 or later is an episode row.

    :param tr: The table row to check.
    :return: True if row is for an episode. False otherwise.
    """
    tds = tr.find_all("td")
    return tds and len(tds) == 3 or (len(tds) == 2 and tds[1].get("colspan") == "2")


def get_burger(tag: Tag, season_number: int) -> Optional[Burger]:
    """
    Parse burger information from HTML.

    :param tag: The HTML tag to parse.
    :param season_number: The season that the burger appears in.
    :return: The parsed burger information.
    """
    if season_number < 9:
        if type(tag.contents[0]) == Tag and tag.contents[0].name == "ul":
            return

        board_string = tag.find(text=True, recursive=False).strip().split(" - ")
        name = board_string[0]
        explanation = board_string[1] if len(board_string) > 1 else None

        ul = tag.find("ul", recursive=False)
        additional_information = (". ".join(
            [li.text.strip(" \n.") for li in ul.find_all("li", recursive=False)]) + ".") if ul else None
    else:
        tds = tag.find_all("td")
        if len(tds) < 2:
            return
        matches = re.findall(r"[^()]+", tds[-2].text)
        name = matches[0].strip("\" \n")
        explanation = matches[1].strip("\" \n") if len(matches) > 1 else None
        additional_information = tds[-1].text.strip("\" \n")
        if additional_information == "None":
            return

    return Burger(name, explanation, additional_information)


def get_burgers(season_number: int, tag: Tag) -> List[Burger]:
    """
    Get all burgers within the given episode.

    :param season_number: The season number.
    :param tag: The HTML tag of the episode.
    :return: A list of all burgers within the given episode.
    """
    burgers = []
    if season_number < 9:
        for ul in tag.find_next_siblings("ul"):
            if ul:
                if ul.find_previous_sibling("h3") is not tag:
                    break
                burgers.extend([burger for burger in
                                [get_burger(list_item, season_number) for list_item in
                                 ul.find_all("li", recursive=False)] if burger is not None])
    else:
        burger = get_burger(tag, season_number)
        if burger is not None:
            burgers.append(burger)
        for tr in tag.find_next_siblings("tr"):
            if is_episode_tr(tr):
                break
            burger = get_burger(tr, season_number)
            if burger is not None:
                burgers.append(burger)

    return burgers


def get_episode(tag: Tag, episode_number: int, season_number: int) -> Episode:
    """
    Parse episode information from HTML.

    :param tag: The HTML tag to parse.
    :param episode_number: The episode number.
    :param season_number: The season that the episode appears in.
    :return: The parsed episode information.
    """
    name = tag.text.strip() if season_number < 9 else tag.find("td").text.strip("\" \n")
    burgers = get_burgers(season_number, tag)

    return Episode(episode_number, name, burgers)


def get_episodes(season_number: int, tag: Tag) -> List[Episode]:
    """
    Get all episodes within the given season.

    :param season_number: The season number.
    :param tag: The HTML tag of the season header.
    :return: A list of all episodes within the given season.
    """
    episodes = []
    if season_number < 9:
        for episode_number, heading in enumerate(tag.find_next_siblings("h3"), 1):
            if heading.find_previous_sibling("h2") is not tag:
                break
            episodes.append(get_episode(heading, episode_number, season_number))
    else:
        episode_number = 1
        for tr in tag.find_next_sibling("table").find_all("tr")[1:]:
            if is_episode_tr(tr):
                episodes.append(get_episode(tr, episode_number, season_number))
                episode_number += 1

    return episodes


def get_season(tag: Tag) -> Season:
    """
    Parse season information from HTML.

    :param tag: The HTML tag to parse.
    :return: The parsed season information.
    """
    season_number = int(tag.text.strip().split()[-1])
    episodes = get_episodes(season_number, tag)

    return Season(season_number, episodes)


def get_seasons(soup: BeautifulSoup) -> List[Season]:
    """
    Parse seasons from HTML.

    :param soup: The soup to parse seasons from.
    :return: A list of parsed seasons information.
    """
    return [get_season(h2) for h2 in (soup.find("div", "mw-parser-output").find_all("h2", recursive=False)) if
            re.match(r"Season \d+", h2.text)]


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
    seasons = get_seasons(BeautifulSoup(get_html(), 'lxml'))
    pretty_print_seasons(seasons)
    save_as_excel(seasons)


if __name__ == "__main__":
    main()
