'''
Author: Sairaghav (https://github.com/sairaghav)

Description:

'''
import json, requests
import config
from collections import defaultdict

def getInfraData(streets):
    for i in range(len(streets)-1):
        score = 0
        relatedPlaces = defaultdict(list)

        for placeType in config.placesOfInterest:
            place = defaultdict(dict)
            mapFinalUrl = config.mapBaseUrl+"/nominatim/v1/search.php?routeWidth=0.000001&bounded=1&osm_type=way&format=json&key="+config.mapApiKey+"&q="+streets[i]['name']+", milano+["+placeType+"]&addressdetails=0"

            response = requests.get(mapFinalUrl)
            responseData = json.loads(response.text)

            for placeDetail in responseData:
                if (streets[i]['lat'] <= float(placeDetail['lat']) >= streets[i+1]['lat']) and (streets[i]['lng'] <= float(placeDetail['lon']) >= streets[i+1]['lng']):
                    place[placeDetail['display_name']]['lat'] = placeDetail['lat']
                    place[placeDetail['display_name']]['lng'] = placeDetail['lon']

            if len(place.keys()) > 0:
                relatedPlaces[placeType].append(place)
                score += len(place.keys())

        if len(relatedPlaces.keys()) > 0:
            streets[i]['infra_metadata'] = relatedPlaces
            streets[i]['infra_score'] = score #Calculate score based on number of individual places of interest found - need to define better
    return streets