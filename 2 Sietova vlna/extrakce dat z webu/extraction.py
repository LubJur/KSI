import time
from typing import NamedTuple, Optional, Dict, Tuple, List, Any
from collections import deque

from time import sleep
from bs4 import BeautifulSoup
import requests


class FullScrap(NamedTuple):
    # TUTO TRIDU ROZHODNE NEMEN
    linux_only_availability: List[str]
    most_visited_webpage: Tuple[int, str]
    changes: List[Tuple[int, str]]
    params: List[Tuple[int, str]]
    tea_party: Optional[str]

    def as_dict(self) -> Dict[str, Any]:
        return {
            'linux_only_availability': self.linux_only_availability,
            'most_visited_webpage': self.most_visited_webpage,
            'changes': self.changes,
            'params': self.params,
            'tea_party': self.tea_party
        }


def download_webpage(url: str, *args, **kwargs) -> requests.Response:
    """
    Download the page and returns its response by using requests.get
    :param url: url to download
    :return: requests Response
    """
    # TUTO FUNKCI ROZHODNE NEMEN
    print('GET ', url)
    return requests.get(url, *args, **kwargs)


def get_linux_only_availability(base_url: str) -> List[str]:
    """
    Finds all functions that area available only on Linux systems
    :param base_url: base url of the website
    :return: all function names that area available only on Linux systems
    """
    # Tuto funkci implementuj
    pass


def get_most_visited_webpage(base_url: str) -> Tuple[int, str]:
    """
    Finds the page with most links to it
    :param base_url: base url of the website
    :return: number of anchors to this page and its URL
    """
    # https://medium.com/analytics-vidhya/apply-depth-first-search-on-web-scraping-770ba20ba33f
    visited = {}
    to_visit = [base_url]

    while len(to_visit) > 0:
        node = to_visit.pop()
        visited[node] = 1
        sleep(0.2)
        soup = BeautifulSoup(download_webpage(node).content, "html.parser")
        all_a = soup.find_all("a")
        for a in all_a:
            a = a.get("href")
            divided = node.split("/")[:-1]
            full = "/".join(divided) + "/" + a
            if a[:4] != "http" and a[0] != "#" and a != "/" and full not in to_visit and a[:3] != "../" and a[-5:] == ".html":
                if full in visited:
                    visited[full] = visited[full] + 1
                    continue
                to_visit.insert(0, full)
    # https://stackoverflow.com/questions/20453674/how-to-find-the-largest-value-in-a-dictionary-by-comparing-values
    max_visited = max(visited, key=visited.get)
    return (visited[max_visited], max_visited)

def get_changes(base_url: str) -> List[Tuple[int, str]]:
    """
    Locates all counts of changes of functions and groups them by version
    :param base_url: base url of the website
    :return: all counts of changes of functions and groups them by version, sorted from the most changes DESC
    """
    # Tuto funkci implementuj
    pass


def get_most_params(base_url: str) -> List[Tuple[int, str]]:
    """
    Finds the function that accepts more than 10 parameters
    :param base_url: base url of the website
    :return: number of parameters of this function and its name, sorted by the count DESC
    """
    # Tuto funkci implementuj
    pass


def find_secret_tea_party(base_url: str) -> Optional[str]:
    """
    Locates a secret Tea party
    :param base_url: base url of the website
    :return: url at which the secret tea party can be found
    """
    # Tuto funkci implementuj
    # https://medium.com/analytics-vidhya/apply-depth-first-search-on-web-scraping-770ba20ba33f
    visited = []
    to_visit = [base_url]

    while len(to_visit) > 0:
        node = to_visit.pop()
        visited.append(node)
        sleep(0.2)
        soup = BeautifulSoup(download_webpage(node).content, "html.parser")
        all_a = soup.find_all("a")
        for a in all_a:
            a = a.get("href")
            # it only changes the last part after / (www.x.com/test/[change]
            divided = node.split("/")[:-1]
            full = "/".join(divided) + "/" + a
            # without .html because it didn't find anything with it, but it takes a lot longer
            if a[:4] != "http" and a[0] != "#" and a != "/" and full not in to_visit and a[:3] != "../":
                to_visit.insert(0, full)
                if requests.get(full).status_code == 418:
                    return full


def scrap_all(base_url: str) -> FullScrap:
    """
    Scrap all the information as efficiently as we can
    :param base_url: base url of the website
    :return: full web scrap of the Python docs
    """
    # Tuto funkci muzes menit, ale musi vracet vzdy tyto data
    scrap = FullScrap(
        linux_only_availability=get_linux_only_availability(base_url),
        most_visited_webpage=get_most_visited_webpage(base_url),
        changes=get_changes(base_url),
        params=get_most_params(base_url),
        tea_party=find_secret_tea_party(base_url)
    )
    return scrap


def main() -> None:
    """
    Do a full scrap and print the results
    :return:
    """
    # Tuto funkci klidne muzes zmenit podle svych preferenci :)
    import json
    time_start = time.time()
    print(json.dumps(scrap_all('https://python.iamroot.eu/').as_dict()))
    print('took', int(time.time() - time_start), 's')


if __name__ == '__main__':
    main()