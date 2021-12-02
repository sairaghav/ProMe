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

def is_street_first_time(street: str, from_date: datetime.datetime, to_date: datetime.datetime) -> List[StreetList]:
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
    queryset = queryset.filter(street=street).filter(source=username)

    return queryset

# Convert all time values to UTC
def get_utc_from_to_date(from_date: str, to_date: str) -> tuple[(datetime.datetime,datetime.datetime)]:
    # Convert input dates from string to datetime and assign default values if ''
    to_date = datetime.datetime.now(datetime.timezone.utc) if to_date == '' else datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc).replace(hour=23, minute=59, second=59)+datetime.timedelta(days=1)
    from_date = to_date - datetime.timedelta(days=config.fetch_news_for_interval_days) if from_date == '' else datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc).replace(hour=0, minute=0)+datetime.timedelta(days=1)
    # Avoid future dates and from_date greater than to_date
    if to_date > datetime.datetime.now(datetime.timezone.utc):
        to_date = datetime.datetime.now(datetime.timezone.utc)
    if from_date > to_date:
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

def calculate_risk_score(results: RiskData, requested_from: datetime.datetime, requested_till: datetime.datetime) -> RiskData:
    risk_score = results._asdict()['risk_score']
    all_tags = results._asdict()['all_tags']

    for tag in all_tags.keys():
        if tag in config.trackingTags.keys():
            risk_score += all_tags[tag]*config.trackingTags[tag]

    #TODO: Change the logic for risk_score calculation. Right now, it's sum of risk scores for individual tags specified in config.py/no. of days evaluated
    risk_score = risk_score/(requested_till-requested_from).days
    
    # Add risk score for street to DB 
    update_street_db(results._asdict()['street'],{ 'risk_score': risk_score })

    # Change risk_score from float to text
    if risk_score <= 0.05: risk_score = 'Safe'
    elif risk_score <= 0.15: risk_score = 'Moderately Unsafe'
    else: risk_score = 'Unsafe'

    return results._replace(risk_score=risk_score)

def update_risk_db(street: str, available_from: datetime.datetime, available_till: datetime.datetime, requested_from: datetime.datetime, requested_till: datetime.datetime) -> RiskData:
    # Check news articles for only the dates that were not analysed already
    if requested_from < available_from:
        # requested_from to requested_till = requested_from to available_from + available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, requested_from, available_from)
            update_street_risk_db(street, available_till, requested_till)
            update_street_db(street,{'news_from': requested_from,'news_till': requested_till})
        # requested_from to available_till = requested_from to available_from + + already available data
        else:
            update_street_risk_db(street, requested_from, available_from)
            update_street_db(street,{'news_from': requested_from})

    else:
        # available_from to requested_till = available_till to requested_till + already available data
        if requested_till > available_till:
            update_street_risk_db(street, available_till, requested_till)
            update_street_db(street,{'news_till': requested_till})

    queryset = StreetRisk.objects.all().filter(street=street).filter(date__range=[requested_from,requested_till])

    return RiskData(street=street,
                    risk_metadata=list(queryset.values()),
                    risk_score=0.0,
                    all_tags={},
                    all_timeline={},
                    all_top_tag={},
                    all_top_timeline={},
                    user_tags={},
                    user_timeline={},
                    user_top_tag={},
                    user_top_timeline={})

def get_risk(street: str, from_date: datetime.datetime, to_date: datetime.datetime) -> dict:
    street_list =  is_street_first_time(street, from_date, to_date)

    # Check already available data range
    available_from, available_till = street_list.news_from, street_list.news_till
    requested_from, requested_till = from_date, to_date

    # Update DB if new data is required
    results = update_risk_db(street, available_from, available_till, requested_from, requested_till)

    # Get top 3 tags and timelines
    results = get_top_tags(results=results)
    results = get_top_timeline(results=results)

    # Calculate and update risk score
    results = calculate_risk_score(results, requested_from, requested_till)

    return results._asdict()

def update_street_db(street: str, update_fields: dict) -> List[StreetList]:
    street_list = StreetList.objects.get(street=street)

    for field_name in update_fields.keys():
        setattr(street_list, field_name, update_fields[field_name])
        street_list.save(update_fields=[field_name])

    return StreetList.objects.get(street=street)

def update_street_risk_db(street: str, from_date: datetime.datetime, to_date: datetime.datetime) -> List[StreetRisk]:
    results = fetch_from_all_sources(street, from_date, to_date)

    for result in results:
        queryset = StreetRisk.objects.all().filter(street=street)
        if len(queryset.filter(date=result.date)) == 0:
            print('Adding to DB for '+street)
            risk = StreetRisk(news=result.title, date=result.date, source=result.source, street=result.street, tags=result.tags, link=result.link)
            risk.save()

    return StreetRisk.objects.all().filter(street=street)

def fetch_soup(url: str) -> BS:
    return BS(requests.get(url).text, "html.parser")

def fetch_from_source(street: str, from_date: datetime.datetime, to_date: datetime.datetime, source: AbstractNewsSource) -> List[News]:
    results = []
    query = NewsQuery(street, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
    pagination_url = source.get_url(query)
    for page in source.parse_page_ids(fetch_soup(pagination_url)):
        query = query._replace(page=page)
        page_url = source.get_url(query)
        for partial_news in source.parse_news_list(fetch_soup(page_url)):
            if not any(tag in config.trackingTags.keys() for tag in partial_news.tags.split(",")):
                continue  # No tag we want is included in the news, skip
            result = source.parse_news_page(fetch_soup(partial_news.link), partial_news)
            result = result._replace(source=source.name, street=street)
            results.append(result)
    return results


# Returns news data for the last few days for a street on specified news URL
def fetch_from_all_sources(street: str, from_date: datetime.datetime, to_date: datetime.datetime) -> List[News]:
    news = []
    for source in config.sources:
        print('Querying '+source.name+' for '+street+' between '+from_date.strftime('%Y-%m-%d %H:%M:%S')+' and '+to_date.strftime('%Y-%m-%d %H:%M:%S'))
        news.extend(fetch_from_source(street, from_date, to_date, source))
    return news
