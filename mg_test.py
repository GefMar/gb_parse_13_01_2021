import os
import requests
import bs4
from urllib.parse import urljoin
from dotenv import load_dotenv

from database import Database



load_dotenv(".env")


start_url = "https://geekbrains.ru/posts"
done_urls = set()

done_urls.add(start_url)
database = Database(os.getenv("SQL_DB_URL"))

def _get_soup(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    return soup

def parse_task(url, callback):
    url = url
    callback = callback
    def wrap():
        soup = _get_soup(url)
        return callback(url, soup)

    return wrap


def post_parse(url, soup: bs4.BeautifulSoup) -> dict:
    author_name_tag = soup.find("div", attrs={"itemprop": "author"})
    data = {
        "post_data": {
            "url": url,
            "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
        },
        "author": {
            "url": urljoin(url, author_name_tag.parent.get("href")),
            "name": author_name_tag.text,
        },
        "tags": [
            {
                "name": tag.text,
                "url": urljoin(url, tag.get("href")),
            }
            for tag in soup.find_all("a", attrs={"class": "small"})
        ],
    }
    return data

def pag_parse(url, soup: bs4.BeautifulSoup):
    gb_pagination = soup.find("ul", attrs={"class": "gb__pagination"})
    a_tags = gb_pagination.find_all("a")
    for a in a_tags:
        pag_url = urljoin(url, a.get("href"))
        if pag_url not in done_urls:
            task = parse_task(pag_url, pag_parse)
            tasks.append(task)
            done_urls.add(pag_url)

    posts_urls = soup.find_all("a", attrs={"class": "post-item__title"})
    for post_url in posts_urls:
        post_href = urljoin(url, post_url.get("href"))
        if post_href not in done_urls:
            task = parse_task(post_href, post_parse)
            tasks.append(task)
            done_urls.add(post_href)


tasks = [parse_task(start_url, pag_parse)]

def run():
    for task in tasks:
        result = task()
        if result:
            database.create_post(result)

run()
