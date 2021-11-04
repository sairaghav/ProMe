import requests
import config
from collections import defaultdict


def is_north_east_of(target, location):
    # Given we are in Italy (North of Equator, East of Greenwich)
    # Why one is lon and other is lng? Can't we have a convention?
    return float(target['lat']) >= location['lat'] and float(target['lon']) >= location['lng']


def collect_on_route(streets):
    for i in range(len(streets) - 1):
        score = 0
        related_places = defaultdict(list)

        for placeType in config.significant_place_types:
            place = defaultdict(dict)
            map_final_url = f"{config.mapBaseUrl}/nominatim/v1/search.php?routeWidth=0.000001&bounded=1&osm_type=way&format=json&key={config.mapApiKey}&q={streets[i]['name']}, milano+[{placeType}]&addressdetails=0"

            response_data = requests.get(map_final_url).json()

            for place_detail in response_data:
                # But why?
                if is_north_east_of(place_detail, streets[i]) and is_north_east_of(place_detail, streets[i + 1]):
                    place[place_detail['display_name']]['lat'] = place_detail['lat']
                    place[place_detail['display_name']]['lng'] = place_detail['lon']

            if place:
                related_places[placeType].append(place)
                score += len(place)

        if related_places:
            streets[i]['infra_metadata'] = related_places
            streets[i]['infra_score'] = score
            # Calculate score based on number of individual places of interest found - need to define better
    return streets
