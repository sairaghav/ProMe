'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Defines the routes for the API: https://developer.mapquest.com/documentation/open/directions-api/route/get/
    /api/directions?from=<source>&to=<destination>: Returns the streets for the quickest drive time
    /api/directions?from=<source>&to=<destination>&mode=pedestrian: Returns the streets for walking route; Avoids limited access roads; Ignores turn restrictions
    /api/directions?from=<source>&to=<destination>&mode=shortest: Returns the streets for the shortest driving distance route
    /api/directions?from=<source>&to=<destination>&mode=bicycle: Returns the streets on which bicycling is appropriate
'''
from typing import NamedTuple
from flask import Flask, request, make_response
from directions import routing, significant_places
from news import risk, news_articles

api = Flask(__name__)


class Response(NamedTuple):
    results: str
    errors: str


@api.route('/api/directions', methods=['GET'])
def directions() -> Response:
    from_src = request.args.get('from', None)
    to_dst = request.args.get('to', None)
    mode = request.args.get('mode', "fastest")

    if from_src is None or to_dst is None:
        response = Response(results=None, errors="Expected Format: /api/directions?from=<source>&to=<destination>&mode=<null|pedestrian|shortest|bicycle>")

    else:
        result = []
        streets = routing.fetch_instructions(from_src, to_dst, mode)
        # streets = significant_places.collect_on_route(streets))

        for street in streets:
            if type(street) == dict:
                response = Response(results=None, errors=street['info']['messages'])
            else:
                result.append(risk.calculate_score(street._asdict()))
                response = Response(results=result, errors=None)
    
    return make_response(response._asdict(), 200)


@api.route('/api/news', methods=['GET'])
def news_of_street() -> Response:
    street_name = request.args.get('street', None)
    from_date = request.args.get('start', None)
    to_date = request.args.get('end', None)

    if street_name is None or from_date is None or to_date is None:
        response = Response(results=None, errors="Expected Format: /api/news?street=<street>&start=<yyyy-mm-dd>&end=<yyyy-mm-dd>")

    else:
        result = []
        for street_news in news_articles.fetch_from_all_sources(street_name, from_date, to_date):
            result.append(street_news._asdict())
            response = Response(results=result, errors=None)

    return make_response(response._asdict(), 200)


if __name__ == '__main__':
    api.run()
