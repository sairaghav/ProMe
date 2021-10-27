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
import json, requests
import urllib.parse
import config

def getStreets(fromSrc,toDst,mode="fastest"):
    fromSrc = urllib.parse.quote_plus(fromSrc)
    toDst = urllib.parse.quote_plus(toDst)

    mapFinalUrl = config.mapBaseUrl + "/directions/v2/route?key=" + config.mapApiKey + "&from=" + fromSrc + "&to=" + toDst + "&routeType="+mode + "&unit=k"
    response = requests.get(mapFinalUrl)
    responseData = json.loads(response.text)

    print(response)
    
    street = {}
    results = []
    #https://developer.mapquest.com/documentation/open/directions-api/route/get/

    if len(responseData['info']['messages']) > 0:
        results.append(responseData)
        return results

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
                results.append(street.copy())

    #Add starting and ending points for the journey
    locations = responseData['route']['locations']

    for i in range(len(locations)):
        street['name'] = locations[i]['street']
        street['narrative'] = 'Starting Point' if i == 0 else "End point"
        street['distance'] = 0
        street['lng'] = locations[i]['latLng']['lng']
        street['lat'] = locations[i]['latLng']['lat']
        street['direction'] = results[0]['direction'] if i == 0 else results[len(results)-1]['direction']
        street['mode'] = results[0]['mode'] if i == 0 else results[len(results)-1]['mode']
        street['risk_score'] = 0
        street['infra_score'] = 0

        results.insert(0,street.copy()) if i == 0 else results.insert(len(results),street.copy())

    return results