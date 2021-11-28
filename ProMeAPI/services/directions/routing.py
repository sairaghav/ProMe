import requests
import urllib.parse
from ProMeAPI.services import config
from typing import NamedTuple, List

from ProMeAPI.services.news.news_articles import RiskData


class Route(NamedTuple):
    direction: str
    distance: int
    infra_score: int
    lat: float
    lng: float
    mode: str
    name: str
    narrative: str
    mapUrl: str
    risk_data: dict

def fetch_route(from_source, to_destination, mode) -> List[Route]:
    from_source = urllib.parse.quote_plus(from_source)
    to_destination = urllib.parse.quote_plus(to_destination)

    map_final_url = f"{config.mapBaseUrl}/directions/v2/route?key={config.mapApiKey}&from={from_source}&to={to_destination}&routeType={mode}&unit=k"
    response_data = requests.get(map_final_url).json()

    results: List[Route] = []
    # https://developer.mapquest.com/documentation/open/directions-api/route/get/

    if 'info' in response_data.keys():
        if len(response_data['info']['messages']) > 0: return [response_data]

    #start_point, *destination_points = response_data['route']['locations']
    # Can we actually have multiple destinations?
    for leg in response_data['route']['legs']:
        for maneuver in leg['maneuvers']:
            if maneuver['streets']:
                lat = maneuver['startPoint']['lat']
                lng = maneuver['startPoint']['lng']
                name = " ".join(maneuver['streets'])
                maneuver_street = Route(name=name, lat=lat, lng=lng, distance=maneuver['distance'],
                                              direction=maneuver['directionName'], mode=maneuver['transportMode'],
                                              infra_score=0, narrative=maneuver['narrative'][:-1], risk_data={}, mapUrl=maneuver['mapUrl'])
                results.append(maneuver_street)

    '''
    # Add the start point for the journey
    start_street = Route(name=start_point["street"], distance=0, lng=start_point["latLng"]["lng"],
                               lat=start_point["latLng"]["lat"], direction=results[0].direction, mode=results[0].mode,
                               risk_score=0, infra_score=0, narrative="Start from starting point", risk_metadata=[], mapUrl='')
    results.insert(0, start_street)
    
    # Add the destination points for the journey
    for destination_point in destination_points:
        destination_street = Route(name=destination_point["street"], distance=0,
                                         lng=destination_point["latLng"]["lng"], lat=destination_point["latLng"]["lat"],
                                         direction=results[-1].direction, mode=results[-1].mode, risk_score=0,
                                         infra_score=0, narrative="Reach end point", risk_metadata=[], mapUrl='')
        results.append(destination_street)
    '''
    return results
