# ProMe

API Prototype for ProMe app
- Uses `https://developer.mapquest.com/` for maps
- Other values provided in [config file](config.py)

**Start with server.py**

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

**Example usage:** http://prome-api.herokuapp.com/directions/Via%20Risorgimento%20237/Piazza%20Leonardo%20da%20Vinci,%20Milan
![sample](examples/images/sample.png)

## TODO
- Improve news article detection and scoring
- User Authentication and DB
- Add infrastructure-related data to street data
- Add more news sources