'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Defines the routes for the API: https://developer.mapquest.com/documentation/open/directions-api/route/get/
    /directions/<fromSrc>/<toDst>: Returns the streets for the quickest drive time
    /directions/pedestrian/<fromSrc>/<toDst>: Returns the streets for walking route; Avoids limited access roads; Ignores turn restrictions
    /directions/shortest/<fromSrc>/<toDst>: Returns the streets for the shortest driving distance route
    /directions/bicycle/<fromSrc>/<toDst>: Returns the streets on which bicycling is appropriate
'''
from flask import Flask, make_response
from map import getDirections, getPlacesOfInterest
from news import getRiskScore

api = Flask(__name__)

results = {}
result = []
noOfDays = 14

@api.route('/directions/<fromSrc>/<toDst>', methods=['GET'])
def directions(fromSrc,toDst):
    streets = getDirections.getStreets(fromSrc,toDst)
    #streets = getPlacesOfInterest.getInfraData(streets)

    for street in streets:
        result.append(getRiskScore.getNewsData(street,noOfDays))

    results['results'] = result

    response = make_response(results,200)

    return response

@api.route('/directions/<modeOfTransport>/<fromSrc>/<toDst>', methods=['GET'])
def directionsMode(fromSrc,toDst,modeOfTransport):
    streets = getDirections.getStreets(fromSrc,toDst,modeOfTransport)
    
    if 'name' in streets[0].keys():
        #streets = getPlacesOfInterest.getInfraData(streets)

        for street in streets:
            result.append(getRiskScore.getNewsData(street,noOfDays))
    else:
        result.append(streets)

    results['results'] = result

    response = make_response(results,200)

    return response

if __name__ == '__main__':
    api.run()