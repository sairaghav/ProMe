'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Defines the routes for the API: https://developer.mapquest.com/documentation/open/directions-api/route/get/
    /directions/<fromSrc>/<toDst>: Returns the streets for the quickest drive time
    /directions/pedestrian/<fromSrc>/<toDst>: Returns the streets for walking route; Avoids limited access roads; Ignores turn restrictions
    /directions/shortest/<fromSrc>/<toDst>: Returns the streets for the shortest driving distance route
    /directions/bicycle/<fromSrc>/<toDst>: Returns the streets on which bicycling is appropriate
'''
from flask import Flask, make_response
from map import routing, significant_places
from news import risk, news_articles

api = Flask(__name__)


@api.route('/directions/<from_src>/<to_dst>', methods=['GET'])
def directions(from_src, to_dst):
    result = []

    streets = routing.fetch_instructions(from_src, to_dst)
    # streets = significant_places.collect_on_route(streets)

    if 'name' in streets[0]:
        for street in streets:
            result.append(risk.calculate_score(street))
    else:
        result.append(streets)

    results = {'results': result}

    return make_response(results, 200)


@api.route('/directions/<mode_of_transport>/<from_src>/<to_dst>', methods=['GET'])
def directions_with_mode(from_src, to_dst, mode_of_transport):
    result = []

    streets = routing.fetch_instructions(from_src, to_dst, mode_of_transport)

    if 'name' in streets[0]:
        # streets = significant_places.collect_on_route(streets)

        for street in streets:
            result.append(risk.calculate_score(street))
    else:
        result.append(streets)

    return make_response({
        "results": result
    }, 200)


@api.route('/news/<street_name>/<from_date>/<to_date>', methods=['GET'])
def news_of_street(street_name: str, from_date: str, to_date: str):
    street_news = news_articles.fetch_from_all_sources(street_name, from_date, to_date)

    return make_response({
        street_name: street_news
    }, 200)


if __name__ == '__main__':
    api.run()
