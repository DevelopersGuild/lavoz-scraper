from typing import Dict, Union, List
import requests
from dateutil import parser
from lxml import html

HTTP_HEADERS: Dict[str, str] = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def get_page_length() -> Union[int, None]:
    """Fetches the amount of available pages in the Lavoz news directory."""
    response = requests.get("https://lavozdeanza.com/category/news",
                            headers=HTTP_HEADERS)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        page_length: str = tree.cssselect(
            '#fullhomepage div.navigation ol li:nth-child(10) a')[0].text
        return int(page_length)
    else:
        raise ValueError(
            'Something went wrong when fetching the page length information.')


def get_link_data(target: int) -> Union[List[Dict[str, str]], None]:
    """ Retrieves links from a specific La Voz directory page."""
    response = requests.get(
        f"https://lavozdeanza.com/category/news/page/{target}/",
        headers=HTTP_HEADERS)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        links = tree.cssselect('#contentleft div div h2 a')
        return [{"href": i.attrib['href'], "content": i.text} for i in links]
    else:
        raise ValueError(
            'Something went wrong when fetching the link information.')


def get_story_data(url: str) -> Union[Dict[str, Union[str, List[str]]], None]:
    """Fetches Story Content from a La Voz story and returns a dictionary with it."""
    response = requests.get(url, headers=HTTP_HEADERS)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        headline = tree.cssselect('#contentleft div.postarea div h1')[0].text
        by = tree.cssselect(
            '#contentleft div.postarea div div.storydetails p span.storybyline'
        )[0].text
        date = tree.cssselect(
            '#contentleft div.postarea div div.storydetails p span.storydate span'
        )[0].text
        tags = [
            i.text for i in tree.cssselect(
                '#contentleft div.postarea ul.snotags li a')
        ]
        ps = tree.cssselect('#contentleft div.postarea div span div p');
        ss = tree.cssselect(
                    '#contentleft div.postarea div span div p span')
        content = [i.text for i in ps] if ps[0].text != None else [i.text for i in ss]
        return {
            "headline": headline,
            "by": by,
            "date": parser.parse(date),
            "tags": tags,
            "content": content,
            "href": url
        }
    else:
        raise ValueError(
            'Something went wrong when fetching the story information.')