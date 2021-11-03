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
from news import getRiskScore, getNewsArticles

api = Flask(__name__)

@api.route('/directions/<fromSrc>/<toDst>', methods=['GET'])
def directions(fromSrc,toDst):
    results = {}
    result = []
    
    streets = getDirections.getStreets(fromSrc,toDst)
    #streets = getPlacesOfInterest.getInfraData(streets)

    if 'name' in streets[0].keys():
        for street in streets:
            result.append(getRiskScore.calcRiskScore(street))
    else:
        result.append(streets)

    results['results'] = result

    response = make_response(results,200)

    return response

@api.route('/directions/<modeOfTransport>/<fromSrc>/<toDst>', methods=['GET'])
def directionsMode(fromSrc,toDst,modeOfTransport):
    results = {}
    result = []
    
    streets = getDirections.getStreets(fromSrc,toDst,modeOfTransport)
    
    if 'name' in streets[0].keys():
        #streets = getPlacesOfInterest.getInfraData(streets)

        for street in streets:
            result.append(getRiskScore.calcRiskScore(street))
    else:
        result.append(streets)

    results['results'] = result

    response = make_response(results,200)

    return response

@api.route('/news/<streetName>/<fromDate>/<toDate>', methods=['GET'])
def newsStreet(streetName,fromDate,toDate):
    results = {}

    street = {}
    street['name'] = streetName
    results[streetName] = getNewsArticles.collect_all(street, fromDate, toDate)

    response = make_response(results,200)

    return response

if __name__ == '__main__':
    api.run()