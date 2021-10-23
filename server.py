from flask import Flask, make_response
import getDirections

api = Flask(__name__)

@api.route('/directions/<fromSrc>/<toDst>', methods=['GET'])
def directions(fromSrc,toDst):
    headers = {"Content-Type": "application/json"}

    streets = getDirections.getStreets(fromSrc,toDst)

    results = {}
    result = []

    for street in streets:
        result.append(getDirections.getNewsData(street))

    results['result'] = result

    return make_response(
        results,
        200
    )

@api.route('/directions/pedestrian/<fromSrc>/<toDst>', methods=['GET'])
def directionsPedestrian(fromSrc,toDst):
    headers = {"Content-Type": "application/json"}

    streets = getDirections.getStreets(fromSrc,toDst,"pedestrian")

    results = {}
    result = []

    for street in streets:
        result.append(getDirections.getNewsData(street))

    results['result'] = result

    return make_response(
        results,
        200
    )

@api.route('/directions/shortest/<fromSrc>/<toDst>', methods=['GET'])
def directionsShortest(fromSrc,toDst):
    headers = {"Content-Type": "application/json"}

    streets = getDirections.getStreets(fromSrc,toDst,"shortest")

    results = {}
    result = []

    for street in streets:
        result.append(getDirections.getNewsData(street))

    results['result'] = result

    return make_response(
        results,
        200
    )

if __name__ == '__main__':
    api.run()