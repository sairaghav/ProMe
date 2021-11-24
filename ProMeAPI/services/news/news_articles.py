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
import requests, datetime
from bs4 import BeautifulSoup as BS
from .parsers.classes import *

from ProMeAPI.services import config
from ProMeAPI.services.news.parsers.classes import News
from ProMeAPI.models import StreetRisk, StreetList

def get_risk_score(street: str, from_date: str, to_date: str, format='text') -> str:
    try:
        street_list = StreetList.objects.get(street=street)
        if street_list.news_from == from_date and street_list.news_till == to_date:
            risk_score = street_list.risk_score
        else:
            get_news_articles(street, from_date, to_date)
            street_list = StreetList.objects.get(street=street)
            risk_score = street_list.risk_score
    
    except StreetList.DoesNotExist:
        get_news_articles(street, from_date, to_date)
        street_list = StreetList.objects.get(street=street)
        risk_score = street_list.risk_score

    if format == 'text':
        if risk_score <= 0.05: risk_score = 'Safe'
        elif risk_score <= 0.25: risk_score = 'Moderately Safe'
        else: risk_score = 'Unsafe'

        return risk_score

    else:
        return str(risk_score)

def is_street_first_time(street: str) -> List[StreetList]:
    try:
        street_list = StreetList.objects.get(street=street)
        return street_list

    except StreetList.DoesNotExist:
        return None

def add_user_reported_incidents(street: str, summary: str, tags: str, user='Test') -> List[StreetRisk]:
    username = 'User '+user
    risk = StreetRisk(news=summary, date=datetime.datetime.now(datetime.timezone.utc), source=username, street=street, tags=tags, link='')
    risk.save()

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)
    queryset = queryset.filter(source=username)

    return queryset

# Convert all time values to UTC
def get_utc_from_to_date(from_date: str, to_date: str) -> tuple[(datetime.datetime,datetime.datetime)]:
    # Convert input dates from string to datetime and assign default values if None
    from_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days) if from_date is None else datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=1)
    to_date = datetime.datetime.now(datetime.timezone.utc) if to_date is None else datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=1)

    # Avoid future dates and from_date greater than to_date
    if to_date > datetime.datetime.now(datetime.timezone.utc) or from_date < to_date:
        to_date = datetime.datetime.now(datetime.timezone.utc)
        from_date = to_date - datetime.timedelta(days=config.fetch_news_for_interval_days)

    return from_date, to_date

def get_news_articles(street: str, from_date: str, to_date: str) -> List[StreetRisk]:
    street_list =  is_street_first_time(street)

    if street_list is None:
        street_list = add_to_street_db(street,{'street': street, 'news_from': from_date,'news_till': to_date, 'risk_score': 0.0})

    # Check already available data range
    available_from, available_till = get_utc_from_to_date(street_list.news_from, street_list.news_till)
    requested_from, requested_till = get_utc_from_to_date(from_date, to_date)

    time_range = (available_till - available_from).days

    # Check news articles for only the dates that were not analysed already
    if requested_from < available_from:
        # requested_from to requested_till = requested_from to available_from + available_till to requested_till + already available data
        if requested_till > available_till:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            add_to_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d'),'news_till': requested_till.strftime('%Y-%m-%d')})
            time_range = (requested_till - requested_from).days
        # requested_from to available_till = requested_from to available_from + + already available data
        else:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d')})
            time_range = (available_till - requested_from).days

    else:
        # available_from to requested_till = available_till to requested_till + already available data
        if requested_till > available_till:
            add_to_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            add_to_street_db(street,{'news_till': requested_till.strftime('%Y-%m-%d')})
            time_range = (requested_till - available_from).days

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)
    queryset = queryset.filter(date__range=[requested_from,requested_till])

    # Add risk score for street to DB
    add_to_street_db(street,{'risk_score': len(queryset)/time_range})

    return queryset


def add_to_street_db(street: str, updatefields: dict) -> List[StreetList]:
    try:
        street_list = StreetList.objects.get(street=street)

        for field_name in updatefields.keys():
            setattr(street_list, field_name, updatefields[field_name])
            street_list.save(update_fields=[field_name])

    # Add street data if not already present
    except StreetList.DoesNotExist:
        add_to_risk_db(street, updatefields['news_from'], updatefields['news_till'])
        
        street_list = StreetList(street=updatefields['street'],news_from=updatefields['news_from'],news_till=updatefields['news_till'])
        street_list.save()
        
    return street_list

def add_to_risk_db(street: str, from_date: str, to_date: str) -> List[News]:
    results = fetch_from_all_sources(street, from_date, to_date)
    from_date, to_date = get_utc_from_to_date(from_date, to_date)

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)

    for result in results:
        if len(queryset.filter(link=result.link)) == 0:
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
