'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Defines the routes for the API: https://developer.mapquest.com/documentation/open/directions-api/route/get/
    /directions/<fromSrc>/<toDst>: Returns the streets for the quickest drive time
    /directions/pedestrian/<fromSrc>/<toDst>: Returns the streets for walking route; Avoids limited access roads; Ignores turn restrictions
    /directions/shortest/<fromSrc>/<toDst>: Returns the streets for the shortest driving distance route
    /directions/bicycle/<fromSrc>/<toDst>: Returns the streets on which bicycling is appropriate
'''
from flask import Flask, make_response
import getDirections
from news import getMilanoToday

api = Flask(__name__)

results = {}
result = []
noOfDays = 30

@api.route('/directions/<fromSrc>/<toDst>', methods=['GET'])
def directions(fromSrc,toDst):
    streets = getDirections.getStreets(fromSrc,toDst)

    for street in streets:
        result.append(getDirections.getNewsData(street,noOfDays))

    results['result'] = result

    return make_response(
        results,
        200
    )

@api.route('/directions/<modeOfTransport>/<fromSrc>/<toDst>', methods=['GET'])
def directionsPedestrian(fromSrc,toDst,modeOfTransport):
    streets = getDirections.getStreets(fromSrc,toDst,modeOfTransport)

    for street in streets:
        result.append(getMilanoToday.getNewsData(street,noOfDays))

    results['result'] = result

    return make_response(
        results,
        200
    )

if __name__ == '__main__':
    api.run()