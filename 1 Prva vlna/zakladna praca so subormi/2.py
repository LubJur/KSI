from typing import Tuple, List, Callable, Dict, NamedTuple
import json
"""
class Meme(NamedTuple):
    def __init__(self, postLink: str, subreddit: str,
                title: str,
                url: str,
                nsfw: bool,
                spoiler: bool,
                author: str,
                ups: int,
                preview: List[str]):
        self.postLink: str = postLink
        self.subreddit: str = subreddit
        self.title: str = title
        self.url: str = url
        self.nsfw: bool = nsfw
        self.spoiler: bool = spoiler
        self.author: str = author
        self.ups: int = ups
        self.preview: List[str] = preview


class Memes(NamedTuple):
    count: int
    memes: List[Meme]

def get_best_meme(memes: List[Meme], filter: Callable[[Meme], bool]) -> Meme:
    # TODO
    pass

def get_subreddit_memes_ratings(memes: List[Meme], subreddit: str) -> List[int]:
    # TODO
    pass

def get_all_subreddits(memes: List[Meme]) -> List[str]:
    # TODO
    pass
"""
def load_memes(fileName: str):
    obj = json.load(fileName)
    return obj
    pass

def analyze_memes(fileName: str) -> Tuple[str, str, str]:
    with open(fileName, "r") as file:
        obj = json.load(file)

    dict_of_subs = {}
    for i in obj["memes"]:
        if i["subreddit"] not in dict_of_subs:
            dict_of_subs.update({i["subreddit"]: i["ups"]})
            dict_of_subs.update({i["subreddit"] + "_count": 1})
        else:
            dict_of_subs.update({i["subreddit"]: dict_of_subs.get(i["subreddit"]) + i["ups"]})
            dict_of_subs.update({i["subreddit"]+"_count": dict_of_subs.get(i["subreddit"]+"_count") + 1})
    print(dict_of_subs)

    average_of_subs = {}
    for i in dict_of_subs:
        if "_count" not in i:
            print("average of sub", i, "is", dict_of_subs[i]/dict_of_subs[i+"_count"])
            average_of_subs.update({i: dict_of_subs[i]/dict_of_subs[i+"_count"]})
            print(average_of_subs)
    max_average_sub = max(average_of_subs.items(), key=lambda x: x[0])  # https://stackoverflow.com/questions/53604668/finding-highest-value-in-a-dictionary
    max_average_sub = max_average_sub[0]
    print(max_average_sub)

    ups_before = 0
    now_meme = {}
    for i in obj["memes"]:
        if i["subreddit"] == max_average_sub:
            if i["ups"] > ups_before:
                now_meme = i
                ups_before = i["ups"]
                print(now_meme["url"])

    ups_before_2 = 0
    now_meme_2 = {}
    for i in obj["memes"]:
        if i["ups"] > ups_before_2:
            now_meme_2 = i
            ups_before_2 = i["ups"]
    print(now_meme_2["url"])

    # název subredditu, jejichž memes mají v průměru nejlepší hodnocení
    # odkaz na meme z vráceného subredditu, který má nejlepší hodnocení
    # odkaz na meme s nejlepším hodnocením vůbec
    return (max_average_sub, now_meme["postLink"], now_meme_2["postLink"])


print(analyze_memes("memes.json"))
