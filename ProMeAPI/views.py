
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ProMeAPI.services.news import news_articles
from ProMeAPI.services.directions import routing
from ProMeAPI.services import config

from typing import NamedTuple

class Response(NamedTuple):
    results: str
    errors: str

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_risk_data(request) -> JsonResponse:
    street = request.GET.get('street', None)
    from_date, to_date = [date.strftime('%Y-%m-%d') for date in news_articles.get_utc_from_to_date(request.GET.get('from', None), request.GET.get('to', None))]

    if street is not None:
        response = Response(results=news_articles.get_risk(street, from_date, to_date), errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/getriskdata?street=<street>&from=<from_date_yyyy-mm-dd>&to=<to_date_yyyy-mm-dd>")

    return JsonResponse(response._asdict())

def index(request) -> HttpResponse:
    response = Response(results="Welcome to the ProMe API index page!", errors=None)
    return JsonResponse(response._asdict())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tags(request):
    response = Response(results=config.trackingTags.keys() ,errors=None)

    return JsonResponse(response._asdict())

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
                #route = route._replace(risk_data=news_articles.get_risk(route.name, from_date, to_date))
                result.append(route._asdict())
            
                response = Response(results=result, errors=None)

    else:
        response = Response(results=None, errors="Expected Format: /api/directions?start=<source>&end=<destination>&mode=<null|pedestrian|fastest|bicycle>")
    
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
        response = Response(results=None, errors="Missing required parameters for /api/report. Expected POST parameters: street, summary, tags, user")

    return JsonResponse(response._asdict())
    