'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns the streets between source and destination with risk_score calculated by scraping news articles and tags

getStreets(from, to, modeOfTransport): Returns the following fields for all the streets between a source and destination
    name: Name of street
    distance: Distance to travel in miles
    lng: Longitude of starting point
    lat: Latitude of starting point
    direction: Direction to travel along
    mode: Mode of transport (AUTO, WALK, BICYCLE)
    risk_score: Score calculated initialized to 0


getNewsData(street,noOfDays): Returns risk_score and metadata of news articles/tags for specified noOfDays for a single street name
    risk_score: Score calculated by sum of articles returned
    metadata: Dict of links to news articles and related tag
'''
import json, requests, datetime
import urllib.parse
from bs4 import BeautifulSoup as BS
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
                street['name'] = maneuver['streets'][0]
                street['distance'] = maneuver['distance']
                street['lng'] = maneuver['startPoint']['lng']
                street['lat'] = maneuver['startPoint']['lat']
                street['direction'] = maneuver['directionName']
                street['mode'] = maneuver['transportMode']
                street['risk_score'] = 0
                result.append(street.copy())


    return result

#Returns news data for the last few days for a street on specified news URL
def getNewsData(street,noOfDays):
    relatedNews = {}

    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.datetime.now() - datetime.timedelta(days = noOfDays)).strftime("%Y-%m-%d") #timedelta specified to 30 days

    url = config.newsBaseUrl+"/search/query/"+street['name'].replace(' ','+')+"/from/"+startDate+"/to/"+endDate
    response = requests.get(url)

    soup = BS(response.text,'html.parser')

    for article in soup.findAll('article', attrs={'data-channel':'/notizie/'}):
        for div in article.findAll('div', attrs={'class':'c-story__content'}):
            for listitem in div.findAll('ul'):
                for li in listitem.findAll('li'):
                    tagValue = li.find('a')['href'].replace('/tag/','')[:-1]
                    #Check if only the news with interested tags are taken into consideration
                    if tagValue.lower() in config.trackingTags:
                        relatedNews[config.newsBaseUrl+div.find('header').find('a')['href']] = list()
                        relatedNews[config.newsBaseUrl+div.find('header').find('a')['href']].append(tagValue)
    if len(relatedNews.keys()) > 0:
        street['metadata'] = relatedNews
        street['risk_score'] = len(relatedNews.keys()) #Calculate score based on number of articles - need to define better
    
    return street