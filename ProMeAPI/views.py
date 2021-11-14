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

def add_to_db(street: str, queryset: QuerySet, from_date: str, to_date: str) -> list[News]:
    results = news_articles.fetch_from_all_sources(street, from_date, to_date)

    for result in results:
        if len(queryset.filter(date=result.date, link=result.link)) == 0:
            print('Adding to DB for '+street)
            risk = StreetRisk(news=result.title, date=result.date, source=result.source, street=result.street, tags=result.tags, link=result.link)
            risk.save()

    return results

def index(request) -> HttpResponse:
    return HttpResponse("Hello! You're at the ProMeAPI index.")

def get_news(request) -> JsonResponse:
    street = request.GET.get('street',None)
    from_date = request.GET.get('from',(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime('%Y-%m-%d'))
    to_date = request.GET.get('to',datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'))
    
    # Avoid future dates
    if datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc) <= datetime.datetime.now(datetime.timezone.utc):
        to_date = to_date
    else:
        to_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')

    if street is not None:
        # Check if data for street is already evaluated
        queryset = StreetList.objects.all()
        queryset = queryset.filter(street=street)

        # Add the dates that were checked for news for the street to the DB
        if len(queryset) == 0:
            street_list = StreetList(street=street,news_from=from_date,news_till=to_date)
            street_list.save()

        available_from = datetime.datetime.strptime(queryset.filter(street=street).values('news_from')[0]['news_from'], '%Y-%m-%d').astimezone(datetime.timezone.utc)
        available_till = datetime.datetime.strptime(queryset.filter(street=street).values('news_till')[0]['news_till'], '%Y-%m-%d').astimezone(datetime.timezone.utc)

        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').astimezone(datetime.timezone.utc)

        queryset = StreetRisk.objects.all()
        
        # Check news articles for only the dates that were not analysed already
        street_list = StreetList.objects.get(street=street)
        if from_date < available_from:
            if to_date > available_till:
                add_to_db(street, queryset, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
                street_list.news_from = from_date.strftime('%Y-%m-%d')
                street_list.news_till = to_date.strftime('%Y-%m-%d')
                street_list.save(update_fields=['news_from', 'news_till'])
            else:
                add_to_db(street, queryset, from_date.strftime('%Y-%m-%d'), available_till.strftime('%Y-%m-%d'))
                street_list.news_from = from_date.strftime('%Y-%m-%d')
                street_list.save(update_fields=['news_from'])

        else:
            if to_date > available_till:
                add_to_db(street, queryset, available_till.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
                street_list.news_till = to_date.strftime('%Y-%m-%d')
                street_list.save(update_fields=['news_till'])

            else:
                add_to_db(street, queryset, from_date, to_date)
        
        
        queryset = StreetRisk.objects.all()
        queryset = queryset.filter(street=street,date__range=[from_date,to_date])

        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/news?street=<street>&from=<from_date_yyyy-mm-dd>&to=<to_date_yyyy-mm-dd>")

    return JsonResponse(response._asdict())

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
                    results = add_to_db(street, queryset, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
                    street_visited.append(street)
                    route = route._replace(risk_metadata=[result._asdict() for result in results])
                    route = route._replace(risk_score=len(results))

                else:
                    route = route._replace(risk_metadata=list(queryset.values()))
                    route = route._replace(risk_score=len(queryset))

                result.append(route._asdict())
            
            response = Response(results=result, errors=None)

        return JsonResponse(response._asdict())

    else:
        response = Response(results=None, errors="Expected Format: /api/directions?start=<source>&end=<destination>&mode=<null|pedestrian|shortest|bicycle>")
        return JsonResponse(response._asdict())