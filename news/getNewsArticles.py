'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

getNewsData(street,startDate,endDate): Returns news articles/tags between specified startDate and endDate for a single street name

    Input:
        street (dict): 
            street['name'] = string

        startDate (string): yyyy-mm-dd
        endDate (string): yyyy-mm-dd

    Returns:
        relatedNews (list of dict):
            news['street']: Name of street
            news['source]: Source of news
            news['tags']: Associated tags
            news['link']: Link for news article
            news['date']: Date of news article
            news['time']: Time of news article


getMilanoToday(street,startDate,endDate): Scraps the search results for MilanoToday between the specified dates on the street and 
                                          returns dict with links of articles tagged with the tags specified in config.py
    
    Input:
        street (dict): 
            street['name'] = string

        startDate (string): yyyy-mm-dd
        endDate (string): yyyy-mm-dd

    Returns:
        relatedNews (list of dict):
            news['street']: Name of street
            news['source]: Source of news
            news['tags']: Associated tags
            news['link']: Link for news article
            news['date']: Date of news article
            news['time']: Time of news article
'''

import config
import requests
from bs4 import BeautifulSoup as BS
from .parsers.classes import *


def fetch_soup(url: str) -> BS:
    return BS(requests.get(url).text, "html.parser")


def collect(street: str, start_date: str, end_date: str, source: AbstractNewsSource) -> List[News]:
    results = []
    query = NewsQuery(street, start_date, end_date)
    pagination_url = source.get_url(query)
    for page in source.parse_page_ids(fetch_soup(pagination_url)):
        query = query._replace(page=page)
        page_url = source.get_url(query)
        for partial_news in source.parse_news_list(fetch_soup(page_url)):
            if not any(tag in config.trackingTags for tag in partial_news.tags):
                continue  # No tag we want is included in the news, skip
            result = source.parse_news_page(fetch_soup(partial_news.link), partial_news)
            result = result._replace(source=source.name, street=street)
            results.append(result)
    return results


# Returns news data for the last few days for a street on specified news URL
def collect_all(street, start_date, end_date):
    news = []
    for source in config.sources:
        news.append(collect(street, start_date, end_date, source))
    return news
