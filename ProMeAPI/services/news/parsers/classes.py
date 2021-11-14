from typing import NamedTuple, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote as url_encode


class NewsQuery(NamedTuple):
    street: str
    start_date: str
    end_date: str
    page: Optional[str] = None


class News(NamedTuple):
    date: str
    source: str
    street: str
    tags: str
    link: str
    title: str


class AbstractNewsSource:
    name: str
    _base_url: str

    @staticmethod
    def parse_news_page(soup: BeautifulSoup, partial: Optional[News]) -> News:
        raise NotImplementedError()

    @staticmethod
    def parse_news_list(soup: BeautifulSoup) -> List[News]:
        raise NotImplementedError()

    @staticmethod
    def parse_page_ids(soup: BeautifulSoup) -> List[str]:
        raise NotImplementedError()

    @staticmethod
    def get_url(query: NewsQuery) -> str:
        raise NotImplementedError()
