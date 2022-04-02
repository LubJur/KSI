import time
from typing import NamedTuple, Optional, Dict, Tuple, List, Any
from collections import deque

from time import sleep
from bs4 import BeautifulSoup
import requests

visited = []
to_visit = []
while len(to_visit) > 0:
    node = to_visit.pop()
    soup = Bea