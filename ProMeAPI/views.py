from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse

from ProMeAPI.services.news import news_articles
from ProMeAPI.services.directions import routing
from ProMeAPI.services import config
from ProMeAPI.services.news.parsers.classes import News
from .models import StreetRisk, StreetList

import datetime

from typing import NamedTuple

class Response(NamedTuple):
    results: str
    errors: str

def get_final_from_to_date(request):
    # Convert all time data to UTC
    from_date = request.GET.get('from',(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime('%Y-%m-%d'))
    to_date = request.GET.get('to',datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'))
    
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
    return from_date, (datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)+datetime.timedelta(days=2)).strftime('%Y-%m-%d')

def is_street_first_time(street: str):
    try:
        StreetList.objects.get(street=street)
        first_time_processed = False

    # Add the dates that were checked for news for the street to the DB
    except StreetList.DoesNotExist:
        first_time_processed = True

    return first_time_processed

def get_news_articles(street: str, street_list: QuerySet, requested_from: datetime, requested_till: datetime, available_from: datetime, available_till: datetime) -> QuerySet:
    if requested_from < available_from:
        if requested_till > available_till:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            street_list.news_from = requested_from.strftime('%Y-%m-%d')
            street_list.news_till = requested_till.strftime('%Y-%m-%d')
            street_list.save(update_fields=['news_from', 'news_till'])
        else:
            add_to_risk_db(street, requested_from.strftime('%Y-%m-%d'), available_till.strftime('%Y-%m-%d'))
            street_list.news_from = requested_from.strftime('%Y-%m-%d')
            street_list.save(update_fields=['news_from'])

    else:
        if requested_till > available_till:
            add_to_risk_db(street, available_till.strftime('%Y-%m-%d'), requested_till.strftime('%Y-%m-%d'))
            street_list.news_till = requested_till.strftime('%Y-%m-%d')
            street_list.save(update_fields=['news_till'])

    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street,date__range=[requested_from,requested_till])

    return queryset

def get_news_for_street(request) -> JsonResponse:
    street = request.GET.get('street', None)
    from_date, to_date = get_final_from_to_date(request)
    print(from_date, to_date)
    first_time_processed = is_street_first_time(street)

    if street is not None:
        # Add street data if not already present
        if first_time_processed:
            street_list = StreetList(street=street,news_from=from_date,news_till=to_date)
            street_list.save()
            add_to_risk_db(street, from_date, to_date)

        # Check already available data range
        street_list = StreetList.objects.get(street=street)
        available_from = datetime.datetime.strptime(street_list.news_from, '%Y-%m-%d').astimezone(datetime.timezone.utc)
        available_till = datetime.datetime.strptime(street_list.news_till, '%Y-%m-%d').astimezone(datetime.timezone.utc)

        requested_from = datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)
        requested_till = datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)
        
        # Check news articles for only the dates that were not analysed already
        queryset = get_news_articles(street, street_list, requested_from, requested_till, available_from, available_till)

        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/news?street=<street>&from=<from_date_yyyy-mm-dd>&to=<to_date_yyyy-mm-dd>")

    return JsonResponse(response._asdict())

def add_to_risk_db(street: str, from_date: str, to_date: str) -> list[News]:
    results = news_articles.fetch_from_all_sources(street, from_date, to_date)
    queryset = StreetRisk.objects.all()
    queryset = queryset.filter(street=street,date__range=[from_date,to_date])

    for result in results:
        if len(queryset.filter(date=result.date, link=result.link)) == 0:
            print('Adding to DB for '+street)
            risk = StreetRisk(news=result.title, date=result.date, source=result.source, street=result.street, tags=result.tags, link=result.link)
            risk.save()

    return results

def index(request) -> HttpResponse:
    return HttpResponse("Hello! You're at the ProMeAPI index.")

def get_directions(request) -> JsonResponse:
    start = request.GET.get('start',None)
    end = request.GET.get('end',None)
    mode = request.GET.get('mode','fastest')
    
    to_date = datetime.datetime.now(datetime.timezone.utc)
    from_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)

    if start is not None and end is not None:
        result = []

        routes = routing.fetch_route(start,end,mode)
        street_visited = []
        for route in routes:
            if type(route) == dict:
                response = Response(results=None, errors=route['info']['messages'])
                break
            else:
                street = route.name
                queryset = StreetRisk.objects.all()
                queryset = queryset.filter(street=street,date__range=[from_date,to_date])
            
                if street not in street_visited and len(queryset) == 0:
                    results = add_to_risk_db(street, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
                    street_visited.append(street)
                    route = route._replace(risk_metadata=[result._asdict() for result in results])
                    route = route._replace(risk_score=len(results))

                else:
                    route = route._replace(risk_metadata=list(queryset.values()))
                    route = route._replace(risk_score=len(queryset))

                result.append(route._asdict())
            
            response = Response(results=result, errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/directions?start=<source>&end=<destination>&mode=<null|pedestrian|shortest|bicycle>")
    
    return JsonResponse(response._asdict())

def incident_report(request) -> JsonResponse:
    street = request.GET.get('street', None)
    news = request.GET.get('summary', None)
    tags = request.GET.get('tags', None)

    if street is not None and news is not None and tags is not None:
        risk = StreetRisk(news=news, date=datetime.datetime.now(datetime.timezone.utc), source='User', street=street, tags=tags, link='')
        risk.save()

        queryset = StreetRisk.objects.all()
        queryset = queryset.filter(street=street,news=news,tags=tags)

        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/report?street=<street_name>&summary=<report_summary>&tags=<tag1,tag2>")

    return JsonResponse(response._asdict())
    