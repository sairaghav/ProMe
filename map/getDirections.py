'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns the streets between source and destination

getStreets(from, to, modeOfTransport): Returns the following fields for all the streets between a source and destination
    name: Name of street
    distance: Distance to travel in miles
    lng: Longitude of starting point
    lat: Latitude of starting point
    direction: Direction to travel along
    mode: Mode of transport (AUTO, WALK, BICYCLE)
    risk_score: Score calculated for risk initialized to 0
    infra_score: Score calculated for infrastructure available initialized to 0
'''
import json, requests
import urllib.parse
import config

def getStreets(fromSrc,toDst,mode="fastest"):
    fromSrc = urllib.parse.quote_plus(fromSrc)
    toDst = urllib.parse.quote_plus(toDst)

    mapFinalUrl = config.mapBaseUrl + "/directions/v2/route?key=" + config.mapApiKey + "&from=" + fromSrc + "&to=" + toDst + "&routeType="+mode
    response = requests.get(mapFinalUrl)
    responseData = json.loads(response.text)

    print(responseData)
    
    street = {}
    result = []
    #https://developer.mapquest.com/documentation/open/directions-api/route/get/
    for leg in responseData['route']['legs']:
        for maneuver in leg['maneuvers']:
            if len(maneuver['streets']) > 0:
                street['name'] = '/'.join(maneuver['streets'])
                street['narrative'] = maneuver['narrative']
                street['distance'] = maneuver['distance']
                street['lng'] = maneuver['startPoint']['lng']
                street['lat'] = maneuver['startPoint']['lat']
                street['direction'] = maneuver['directionName']
                street['mode'] = maneuver['transportMode']
                street['risk_score'] = 0
                street['infra_score'] = 0
                result.append(street.copy())


    return result