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
from django.db.models.query import QuerySet
from .. import config
import requests, datetime
from bs4 import BeautifulSoup as BS
from .parsers.classes import *

from ProMeAPI.services.news.parsers.classes import News
from ...models import StreetRisk, StreetList


def add_user_reported_incidents(street: str, summary: str, tags: str) -> QuerySet:
    risk = StreetRisk(news=summary, date=datetime.datetime.now(datetime.timezone.utc), source='User', street=street, tags=tags, link='')
    risk.save()

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street,news=summary,tags=tags)

    return queryset

# Convert all time data to UTC
def get_final_from_to_date(from_date: str, to_date: str):
    # Avoid future dates
    if datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc) <= datetime.datetime.now(datetime.timezone.utc):
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc).strftime('%Y-%m-%d')
    else:
        to_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    
    # Avoid from date greater than to date
    if datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc) < datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc):
        from_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime('%Y-%m-%d')
    else:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc).strftime('%Y-%m-%d')

    # to_date is of %Y-%m-%d format, time is taken as midnight. Converting to UTC reduces date by 1. Hence adding 2 days
    return (datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=2)).strftime('%Y-%m-%d'), (datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=2)).strftime('%Y-%m-%d')

def get_news_articles(street: str, from_date: datetime, to_date: datetime) -> QuerySet:
    street_list = add_to_street_db(street,{'street': street, 'news_from': from_date,'news_till': to_date})

    # Check already available data range
    available_from = datetime.datetime.strptime(street_list.news_from, '%Y-%m-%d').astimezone(datetime.timezone.utc)
    available_till = datetime.datetime.strptime(street_list.news_till, '%Y-%m-%d').astimezone(datetime.timezone.utc)

    requested_from = datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=1)
    requested_till = datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=1)

    print(requested_from, requested_till)

    # Check news articles for only the dates that were not analysed already
    if requested_from < available_from:
        if requested_till > available_till:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'street': street, 'news_from': requested_from.strftime('%Y-%m-%d'),'news_till': requested_till.strftime('%Y-%m-%d')})
        else:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_till.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'street': street, 'news_from': requested_from.strftime('%Y-%m-%d'),'news_till': available_till.strftime('%Y-%m-%d')})

    else:
        if requested_till > available_till:
            add_to_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'street': street, 'news_from': available_from.strftime('%Y-%m-%d'),'news_till': requested_till.strftime('%Y-%m-%d')})
        
    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street,date__range=[requested_from,requested_till])

    return queryset


def add_to_street_db(street: str, updatefields: dict) -> QuerySet:
    try:
        street_list = StreetList.objects.get(street=street)

        for field_name in updatefields.keys():
            setattr(street_list, field_name, updatefields[field_name])
            street_list.save(update_fields=[field_name])

    # Add street data if not already present
    except StreetList.DoesNotExist:
        street_list = StreetList(street=updatefields['street'],news_from=updatefields['news_from'],news_till=updatefields['news_till'])
        street_list.save()
        
    return street_list

def add_to_risk_db(street: str, from_date: str, to_date: str) -> list[News]:
    results = fetch_from_all_sources(street, from_date, to_date)
    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street,date__range=[from_date,to_date])

    for result in results:
        if len(queryset.filter(date=result.date, link=result.link)) == 0:
            print('Adding to DB for '+street)
            risk = StreetRisk(news=result.title, date=result.date, source=result.source, street=result.street, tags=result.tags, link=result.link)
            risk.save()

    return results


def fetch_soup(url: str) -> BS:
    return BS(requests.get(url).text, "html.parser")


def fetch_from_source(street: str, start_date: str, end_date: str, source: AbstractNewsSource) -> List[News]:
    results = []
    query = NewsQuery(street, start_date, end_date)
    pagination_url = source.get_url(query)
    for page in source.parse_page_ids(fetch_soup(pagination_url)):
        query = query._replace(page=page)
        page_url = source.get_url(query)
        for partial_news in source.parse_news_list(fetch_soup(page_url)):
            if not any(tag in config.trackingTags for tag in partial_news.tags.split(",")):
                continue  # No tag we want is included in the news, skip
            result = source.parse_news_page(fetch_soup(partial_news.link), partial_news)
            result = result._replace(source=source.name, street=street)
            results.append(result)
    return results


# Returns news data for the last few days for a street on specified news URL
def fetch_from_all_sources(street: str, start_date: str, end_date: str) -> List[News]:
    news = []
    for source in config.sources:
        print('Querying '+source.name+' for '+street)
        news.extend(fetch_from_source(street, start_date, end_date, source))
    return news
