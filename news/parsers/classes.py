from typing import NamedTuple, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote as url_encode


class NewsQuery(NamedTuple):
    street: str
    start_date: str
    end_date: str
    page: Optional[str] = None


class News(NamedTuple):
    source: str
    link: str
    tags: str
    street: str
    date: str
    time: str


class AbstractNewsSource:
    name: str
    _base_url: str

    def parse_news_page(self, soup: BeautifulSoup, partial: Optional[News]) -> News:
        raise NotImplementedError()

    def parse_news_list(self, soup: BeautifulSoup) -> List[News]:
        raise NotImplementedError()

    def parse_page_ids(self, soup: BeautifulSoup) -> List[str]:
        raise NotImplementedError()

    def get_url(self, *query: NewsQuery) -> str:
        raise NotImplementedError()
