import requests, datetime, collections
from bs4 import BeautifulSoup as BS
from .parsers.classes import *

from ProMeAPI.services import config
from ProMeAPI.services.news.parsers.classes import News
from ProMeAPI.models import StreetRisk, StreetList

class RiskData(NamedTuple):
    street: str
    risk_score: str
    risk_metadata: list
    all_tags: dict
    all_top_tag: dict
    all_timeline: dict
    all_top_timeline: dict
    user_tags: dict
    user_top_tag: dict
    user_timeline: dict
    user_top_timeline: dict

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

def get_top_tags(results: RiskData, limit=3) -> RiskData:
    all_tags = []
    user_tags = []

    for metadata in results._asdict()['risk_metadata']:
        for tag in metadata['tags'].split(','):
            all_tags.append(tag)
            if metadata['source'].lower().startswith('user'):
                user_tags.append(tag)

    return results._replace(
        all_tags=dict(collections.Counter(all_tags)),
        user_tags=dict(collections.Counter(user_tags)),
        all_top_tag=dict(collections.Counter(all_tags).most_common(limit)),
        user_top_tag=dict(collections.Counter(user_tags).most_common(limit))
    )

def get_top_timeline(results: RiskData, limit=3) -> RiskData:
    all_timeline = []
    user_timeline = []

    for metadata in results._asdict()['risk_metadata']:
        date = metadata['date'].strftime('%B %Y')
        all_timeline.append(date)
        if metadata['source'].lower().startswith('user'):
            user_timeline.append(date)

    return results._replace(
        all_timeline=dict(collections.Counter(all_timeline)),
        user_timeline=dict(collections.Counter(user_timeline)),
        all_top_timeline=dict(collections.Counter(all_timeline).most_common(limit)),
        user_top_timeline=dict(collections.Counter(user_timeline).most_common(limit))
    )

def update_risk_db(street: str, available_from: datetime.datetime, available_till: datetime.datetime, requested_from: datetime.datetime, requested_till: datetime.datetime) -> RiskData:
    #time_range = (available_till - available_from).days

    # Check news articles for only the dates that were not analysed already
    if requested_from < available_from:
        # requested_from to requested_till = requested_from to available_from + available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            update_street_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d'),'news_till': requested_till.strftime('%Y-%m-%d')})
            #time_range = (requested_till - requested_from).days
        # requested_from to available_till = requested_from to available_from + + already available data
        else:
            update_street_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_from.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_from': requested_from.strftime('%Y-%m-%d')})
            #time_range = (available_till - requested_from).days

    else:
        # available_from to requested_till = available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            update_street_db(street,{'news_till': requested_till.strftime('%Y-%m-%d')})
            #time_range = (requested_till - available_from).days

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street)
    queryset = queryset.filter(date__range=[requested_from,requested_till])
    
    # Add risk score for street to DB 
    risk_score = len(queryset)/(requested_till-requested_from).days 
    #TODO: Change the logic for risk_score calculation. Right now, it's just no. of articles/no. of days evaluated
    update_street_db(street,{ 'risk_score': risk_score })

    # Change risk_score from float to text
    if risk_score <= 0.05: risk_score = 'Safe'
    elif risk_score <= 0.2: risk_score = 'Moderately Unsafe'
    else: risk_score = 'Unsafe'

    return RiskData(street=street,
                    risk_metadata=list(queryset.values()),
                    risk_score=risk_score,
                    all_tags={},
                    all_timeline={},
                    all_top_tag={},
                    all_top_timeline={},
                    user_tags={},
                    user_timeline={},
                    user_top_tag={},
                    user_top_timeline={})

def get_risk(street: str, from_date: str, to_date: str) -> dict:
    street_list =  is_street_first_time(street, from_date, to_date)

    # Check already available data range
    available_from, available_till = get_utc_from_to_date(street_list.news_from, street_list.news_till)
    requested_from, requested_till = get_utc_from_to_date(from_date, to_date)

    # Update DB if new data is required
    results = update_risk_db(street, available_from, available_till, requested_from, requested_till)

    # Get top 3 tags and timelines
    results = get_top_tags(results)
    results = get_top_timeline(results)

    return results._asdict()

def update_street_db(street: str, update_fields: dict) -> List[StreetList]:
    street_list = StreetList.objects.get(street=street)

    for field_name in update_fields.keys():
        setattr(street_list, field_name, update_fields[field_name])
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
