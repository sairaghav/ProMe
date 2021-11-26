import requests, datetime, collections
from bs4 import BeautifulSoup as BS
from .parsers.classes import *

from ProMeAPI.services import config
from ProMeAPI.services.news.parsers.classes import News
from ProMeAPI.models import StreetRisk, StreetList

def is_street_first_time(street: str, from_date: str, to_date: str) -> List[StreetList]:
    try:
        street_list = StreetList.objects.get(street=street)

    except StreetList.DoesNotExist:
        update_street_risk_db(street, from_date, to_date)
        
        street_list = StreetList(street=street, news_from=from_date, news_till=to_date, risk_score=0.0)
        street_list.save()

    return street_list

def add_user_reported_incidents(street: str, summary: str, tags: str, user) -> List[StreetRisk]:
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
    to_date = datetime.datetime.now(datetime.timezone.utc) if to_date is None else datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(hours=1)
    from_date = to_date - datetime.timedelta(days=config.fetch_news_for_interval_days) if from_date is None else datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(hours=1)
    # Avoid future dates and from_date greater than to_date
    if to_date > datetime.datetime.now(datetime.timezone.utc) or from_date > to_date:
        to_date = datetime.datetime.now(datetime.timezone.utc)
        from_date = to_date - datetime.timedelta(days=config.fetch_news_for_interval_days)

    return from_date, to_date

def update_risk_db(street: str, available_from: datetime, available_till: datetime, requested_from: datetime, requested_till: datetime) -> dict:
    results = {}
    
    time_range = (available_till - available_from).days

    # Check news articles for only the dates that were not analysed already
    if requested_from < available_from:
        # requested_from to requested_till = requested_from to available_from + available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            update_street_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d'),'news_till': requested_till.strftime('%Y-%m-%d')})
            time_range = (requested_till - requested_from).days
        # requested_from to available_till = requested_from to available_from + + already available data
        else:
            update_street_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d')})
            time_range = (available_till - requested_from).days

    else:
        # available_from to requested_till = available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_till': requested_till.strftime('%Y-%m-%d')})
            time_range = (requested_till - available_from).days

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)
    queryset = queryset.filter(date__range=[requested_from,requested_till])
    
    # Add risk score for street to DB
    risk_score = len(queryset)/time_range
    update_street_db(street,{ 'risk_score': risk_score })

    # Change risk_score from float to text
    if risk_score <= 0.05: risk_score = 'Safe'
    elif risk_score <= 0.2: risk_score = 'Slightly Unsafe'
    elif risk_score <= 0.5: risk_score = 'Moderately Unsafe'
    else: risk_score = 'Unsafe'

    results['risk_metadata'] = list(queryset.values())
    results['risk_score'] = risk_score

    return results

def get_risk(street: str, from_date: str, to_date: str) -> dict:
    street_list =  is_street_first_time(street, from_date, to_date)

    # Check already available data range
    available_from, available_till = get_utc_from_to_date(street_list.news_from, street_list.news_till)
    requested_from, requested_till = get_utc_from_to_date(from_date, to_date)

    results = update_risk_db(street, available_from, available_till, requested_from, requested_till)

    # Get top 1, 3 and 5 tags and timelines
    all_metadata = { 'tags': [], 'timeline': [] }
    user_metadata = { 'tags': [], 'timeline': [] }

    for metadata in results['risk_metadata']:
        date = metadata['date'].strftime('%B %Y')
        all_metadata['timeline'].append(date)
        if metadata['source'].lower().startswith('user'):
            user_metadata['timeline'].append(date)

        for tag in metadata['tags'].split(','):
            all_metadata['tags'].append(tag)
            if metadata['source'].lower().startswith('user'):
                user_metadata['tags'].append(tag)

    all_tag_counter = collections.Counter(all_metadata['tags'])
    user_tag_counter = collections.Counter(user_metadata['tags'])
    all_timeline_counter = collections.Counter(all_metadata['timeline'])
    user_timeline_counter = collections.Counter(user_metadata['timeline'])

    results['all_tags'] = dict(all_tag_counter)
    results['all_top_tag_1'] = dict(all_tag_counter.most_common(1))
    results['all_top_tag_3'] = dict(all_tag_counter.most_common(3))
    results['all_top_tag_5'] = dict(all_tag_counter.most_common(5))
    results['user_tags'] = dict(user_tag_counter)
    results['user_top_tag_1'] = dict(user_tag_counter.most_common(1))
    results['user_top_tag_3'] = dict(user_tag_counter.most_common(3))
    results['user_top_tag_5'] = dict(user_tag_counter.most_common(5))

    results['all_timeline'] = dict(all_timeline_counter)
    results['all_top_timeline_1'] = dict(all_timeline_counter.most_common(1))
    results['all_top_timeline_3'] = dict(all_timeline_counter.most_common(3))
    results['all_top_timeline_5'] = dict(all_timeline_counter.most_common(5))
    results['user_timeline'] = dict(user_timeline_counter)
    results['user_top_timeline_1'] = dict(user_timeline_counter.most_common(1))
    results['user_top_timeline_3'] = dict(user_timeline_counter.most_common(3))
    results['user_top_timeline_5'] = dict(user_timeline_counter.most_common(5))

    return results

def update_street_db(street: str, updatefields: dict) -> List[StreetList]:
    street_list = StreetList.objects.get(street=street)

    for field_name in updatefields.keys():
        setattr(street_list, field_name, updatefields[field_name])
        street_list.save(update_fields=[field_name])

def update_street_risk_db(street: str, from_date: str, to_date: str) -> List[News]:
    results = fetch_from_all_sources(street, from_date, to_date)
    from_date, to_date = get_utc_from_to_date(from_date, to_date)

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)
    queryset = queryset.filter(date__range=[from_date, to_date])

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
