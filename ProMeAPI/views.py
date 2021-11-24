
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ProMeAPI.services.news import news_articles
from ProMeAPI.services.directions import routing
from ProMe import config

import collections

from typing import NamedTuple

class Response(NamedTuple):
    results: str
    errors: str

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_risk(request):
    street = request.GET.get('street', None)
    format = request.GET.get('format', 'text')
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(request.GET.get('from', None), request.GET.get('to', None))]

    response = Response(results=news_articles.get_risk_score(street, from_date, to_date, format), errors=None)

    return JsonResponse(response._asdict())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tag_data(request):
    street = request.GET.get('street', None)
    source = request.GET.get('source', 'All')
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(request.GET.get('from', None), request.GET.get('to', None))]
    limit = int(request.GET.get('limit', 0))
    
    data = []

    if street is not None:
        queryset = news_articles.get_news_articles(street, from_date, to_date)
        result = list(queryset.values())

        for value in result:
            to_consider = True
            if source == 'User' and not value['source'].startswith('User'):
                to_consider = False
            else:
                to_consider = True
            if to_consider:
                for tag in value['tags'].split(','):
                    data.append(tag)

        counter = collections.Counter(data)
        if limit > 0:
            counter = counter.most_common(limit)

        response = Response(results=dict(counter), errors=None)
    
    else:
        response = Response(results=None, errors="Expected Format: /api/gettags?street=<street_name>&source=<optional_User>&from=<optional_from_date_yyyy-mm-dd>&to=<optional_to_date_yyyy-mm-dd>&limit=<optional_num_results>")

    return JsonResponse(response._asdict())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timeline_data(request):
    street = request.GET.get('street', None)
    source = request.GET.get('source', 'All')
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(request.GET.get('from', None), request.GET.get('to', None))]
    limit = int(request.GET.get('limit', 0))
    
    data = []

    if street is not None:
        queryset = news_articles.get_news_articles(street, from_date, to_date)
        result = list(queryset.values())

        for value in result:
            to_consider = True
            if source == 'User' and not value['source'].startswith('User'):
                to_consider = False
            if to_consider:
                date = value['date'].strftime('%B %Y')
                data.append(date)

        counter = collections.Counter(data)
        if limit > 0:
            counter = counter.most_common(limit)
        
        response = Response(results=dict(counter), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/gettimeline?street=<street_name>&&source=<optional_User>&from=<optional_from_date_yyyy-mm-dd>&to=<optional_to_date_yyyy-mm-dd>&limit=<optional_num_results>")

    return JsonResponse(response._asdict())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_news_for_street(request) -> JsonResponse:
    street = request.GET.get('street', None)
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(request.GET.get('from', None), request.GET.get('to', None))]

    if street is not None:
        queryset = news_articles.get_news_articles(street, from_date, to_date)
        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/news?street=<street>&from=<from_date_yyyy-mm-dd>&to=<to_date_yyyy-mm-dd>")

    return JsonResponse(response._asdict())

def index(request) -> HttpResponse:
    return HttpResponse("Hello! You're at the ProMeAPI index.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_directions(request) -> JsonResponse:
    start = request.GET.get('start',None)
    end = request.GET.get('end',None)
    mode = request.GET.get('mode','pedestrian')
    
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(None, None)]

    if start is not None and end is not None:
        result = []

        routes = routing.fetch_route(start, end, mode)
        for route in routes:
            if type(route) == dict:
                response = Response(results=None, errors=route['info']['messages'])
                break
            else:
                street = route.name
                route = route._replace(risk_score=news_articles.get_risk_score(street, from_date, to_date))
                result.append(route._asdict())
            
            response = Response(results=result, errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/directions?start=<source>&end=<destination>&mode=<null|pedestrian|shortest|bicycle>")
    
    return JsonResponse(response._asdict())

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_incident(request) -> JsonResponse:
    street = request.POST.get('street', None)
    summary = request.POST.get('summary', None)
    tags = request.POST.get('tags', None)
    user = request.POST.get('user', None)

    if street is not None and summary is not None and tags is not None and user is not None:
        queryset = news_articles.add_user_reported_incidents(street, summary, tags, user)
        response = Response(results=list(queryset.values()), errors=None)

    else:
        response = Response(results=None, errors="Missing required parameters. Expected POST parameters: street, summary, tags, user")

    return JsonResponse(response._asdict())
    