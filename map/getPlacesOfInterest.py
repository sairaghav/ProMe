import requests
import config
from collections import defaultdict


def get_infrastructure_data(streets):
    for i in range(len(streets) - 1):
        score = 0
        related_places = defaultdict(list)

        for placeType in config.placesOfInterest:
            place = defaultdict(dict)
            map_final_url = f"{config.mapBaseUrl}/nominatim/v1/search.php?routeWidth=0.000001&bounded=1&osm_type=way&format=json&key={config.mapApiKey}&q={streets[i]['name']}, milano+[{placeType}]&addressdetails=0"

            response_data = requests.get(map_final_url).json()

            for place_detail in response_data:
                if (streets[i]['lat'] <= float(place_detail['lat']) >= streets[i + 1]['lat']) and (
                        streets[i]['lng'] <= float(place_detail['lon']) >= streets[i + 1]['lng']):
                    place[place_detail['display_name']]['lat'] = place_detail['lat']
                    place[place_detail['display_name']]['lng'] = place_detail['lon']

            if place:
                related_places[placeType].append(place)
                score += len(place.keys())

        if related_places:
            streets[i]['infra_metadata'] = related_places
            streets[i]['infra_score'] = score
            # Calculate score based on number of individual places of interest found - need to define better
    return streets
