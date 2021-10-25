'''
Author: Sairaghav (https://github.com/sairaghav)

Description:

'''
import json, requests
import config
from collections import defaultdict

def getInfraData(streets):
    for street in streets:
        score = 0
        relatedPlaces = defaultdict(list)

        for placeType in config.placesOfInterest:
            place = defaultdict(dict)
            mapFinalUrl = config.mapBaseUrl+"/nominatim/v1/search.php?routeWidth=0.000001&bounded=1&osm_type=way&format=json&key="+config.mapApiKey+"&q="+street['name']+", milano+["+placeType+"]&addressdetails=0&limit=1"

            response = requests.get(mapFinalUrl)
            responseData = json.loads(response.text)

            for placeDetail in responseData:
                place[placeDetail['display_name']]['lat'] = placeDetail['lat']
                place[placeDetail['display_name']]['lng'] = placeDetail['lon']

            if len(place.keys()) > 0:
                relatedPlaces[placeType].append(place)
                score += len(place.keys())

        if len(relatedPlaces.keys()) > 0:
            street['infra_metadata'] = relatedPlaces
            street['infra_score'] = score #Calculate score based on number of individual places of interest found - need to define better
    return streets