# ProMe

API Prototype for ProMe app
- Uses `https://developer.mapquest.com/` for maps
- Other values provided in [config file](config.py)

## Description

Calling `https://prome-api.herokuapp.com/directions/<from>/<to>` returns the route from the source (from) to destination (to), as a list of streets

For each street, following values will be returned:
- name: Name of street
- distance: Distance to travel in miles
- lng: Longitude of starting point
- lat: Latitude of starting point
- direction: Direction to travel along
- mode: Mode of transport (AUTO, WALKING, BICYCLE)
- risk_score: Score calculated for risk based on news articles for the street
- risk_metadata: All news articles and the tags that were associate with them based on new sources
- infra_score: Score calculated for infrastructure available along the street initialized to 0


`https://prome-api.herokuapp.com/directions/pedestrian/<from>/<to>` will return the same values but mode of transport will only be considered as *WALKING*