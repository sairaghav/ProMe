
from django.http import HttpResponse, JsonResponse

from ProMeAPI.services.news import news_articles
from ProMeAPI.services.directions import routing
from ProMe import config

import datetime

from typing import NamedTuple

class Response(NamedTuple):
    results: str
    errors: str

def get_news_for_street(request) -> JsonResponse:
    street = request.GET.get('street', None)
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(
        request.GET.get('from',(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime('%Y-%m-%d')),
        request.GET.get('to',datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'))
        )]
    
    if street is not None:
        queryset = news_articles.get_news_articles(street, from_date, to_date)
        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/news?street=<street>&from=<from_date_yyyy-mm-dd>&to=<to_date_yyyy-mm-dd>")

    return JsonResponse(response._asdict())

def index(request) -> HttpResponse:
    return HttpResponse("Hello! You're at the ProMeAPI index.")

def get_directions(request) -> JsonResponse:
    start = request.GET.get('start',None)
    end = request.GET.get('end',None)
    mode = request.GET.get('mode','pedestrian')
    
    to_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    from_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime('%Y-%m-%d')

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
            
                if street not in street_visited:
                    queryset = news_articles.get_news_articles(street, from_date, to_date)
                    street_visited.append(street)
                
                route = route._replace(risk_metadata=[value for value in queryset.values()])
                route = route._replace(risk_score=len(queryset)/config.fetch_news_for_interval_days)

                result.append(route._asdict())
            
            response = Response(results=result, errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/directions?start=<source>&end=<destination>&mode=<null|pedestrian|shortest|bicycle>")
    
    return JsonResponse(response._asdict())

def report_incident(request) -> JsonResponse:
    if request.method == 'POST':
        street = request.POST.get('street', None)
        news = request.POST.get('summary', None)
        tags = request.POST.get('tags', None)

        if street is not None and news is not None and tags is not None:
            queryset = news_articles.add_user_reported_incidents(street, news, tags)
            response = Response(results=list(queryset.values()), errors=None)

        else:
            response = Response(results=None, errors="Missing required parameters. Expected parameters: street, news, tags")

    else:
            response = Response(results=None, errors="Only POST method supported")

    return JsonResponse(response._asdict())
    