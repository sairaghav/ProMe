'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns the streets between source and destination

getStreets(from, to, modeOfTransport): Returns the following fields for all the streets between a source and destination
    name: Name of street
    distance: Distance to travel in km
    lng: Longitude of starting point
    lat: Latitude of starting point
    direction: Direction to travel along
    mode: Mode of transport (AUTO, WALK, BICYCLE)
    risk_score: Score calculated for risk initialized to 0
    infra_score: Score calculated for infrastructure available initialized to 0
'''

import requests
import urllib.parse
from .. import config
from typing import NamedTuple, List


class Route(NamedTuple):  # TODO: Better name
    direction: str
    distance: int
    infra_score: int
    lat: float
    lng: float
    mode: str
    name: str
    narrative: str
    risk_score: int
    risk_metadata: list


def fetch_route(from_source, to_destination, mode) -> List[Route]:
    from_source = urllib.parse.quote_plus(from_source)
    to_destination = urllib.parse.quote_plus(to_destination)

    map_final_url = f"{config.mapBaseUrl}/directions/v2/route?key={config.mapApiKey}&from={from_source}&to={to_destination}&routeType={mode}&unit=k"
    response_data = requests.get(map_final_url).json()

    results: List[Route] = []
    # https://developer.mapquest.com/documentation/open/directions-api/route/get/

    if response_data['info']['messages']:
        return [response_data]

    start_point, *destination_points = response_data['route']['locations']
    # Can we actually have multiple destinations?
    for leg in response_data['route']['legs']:
        for maneuver in leg['maneuvers']:
            if maneuver['streets']:
                lat = maneuver['startPoint']['lat']
                lng = maneuver['startPoint']['lng']
                name = " ".join(maneuver['streets'])
                maneuver_street = Route(name=name, lat=lat, lng=lng, distance=maneuver['distance'],
                                              direction=maneuver['directionName'], mode=maneuver['transportMode'],
                                              risk_score=0, infra_score=0, narrative=maneuver['narrative'], risk_metadata=[])
                results.append(maneuver_street)

    # Add the start point for the journey
    start_street = Route(name=start_point["street"], distance=0, lng=start_point["latLng"]["lng"],
                               lat=start_point["latLng"]["lat"], direction=results[0].direction, mode=results[0].mode,
                               risk_score=0, infra_score=0, narrative="Starting Point", risk_metadata=[])
    results.insert(0, start_street)

    # Add the destination points for the journey
    for destination_point in destination_points:
        destination_street = Route(name=destination_point["street"], distance=0,
                                         lng=destination_point["latLng"]["lng"], lat=destination_point["latLng"]["lat"],
                                         direction=results[-1].direction, mode=results[-1].mode, risk_score=0,
                                         infra_score=0, narrative="End Point", risk_metadata=[])
        results.append(destination_street)

    return results
