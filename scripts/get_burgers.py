import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    response = requests.get(url)

    if 200 <= response.status_code < 300:
        return response.text

    raise requests.HTTPError(response.reason)


def main():
    soup = BeautifulSoup(get_html("https://bobs-burgers.fandom.com/wiki/Burger_of_the_Day"), 'lxml')
    print(soup.prettify())


if __name__ == "__main__":
    main()
