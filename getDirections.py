import json, requests, datetime
import urllib.parse
from bs4 import BeautifulSoup as BS
import config

def getStreets(fromSrc,toDst):
    fromSrc = urllib.parse.quote_plus(fromSrc)
    toDst = urllib.parse.quote_plus(toDst)

    mapFinalUrl = config.mapBaseUrl + "/directions/v2/route?key=" + config.mapApiKey + "&from=" + fromSrc + "&to=" + toDst# + "&routeType=pedestrian"
    response = requests.get(mapFinalUrl)
    responseData = json.loads(response.text)

    print(responseData)
    
    street = {}
    result = []
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

def getNewsData(street):
    relatedNews = {}

    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime("%Y-%m-%d")

    url = config.newsBaseUrl+"/search/query/"+street['name'].replace(' ','+')+"/from/"+startDate+"/to/"+endDate
    response = requests.get(url)

    soup = BS(response.text,'html.parser')

    for article in soup.findAll('article', attrs={'data-channel':'/notizie/'}):
        for div in article.findAll('div', attrs={'class':'c-story__content'}):
            for listitem in div.findAll('ul'):
                for li in listitem.findAll('li'):
                    tagValue = li.find('a')['href'].replace('/tag/','')[:-1]
                    if tagValue.lower() in config.trackingTags:
                        relatedNews[config.newsBaseUrl+div.find('header').find('a')['href']] = list()
                        relatedNews[config.newsBaseUrl+div.find('header').find('a')['href']].append(tagValue)
    if len(relatedNews.keys()) > 0:
        street['metadata'] = relatedNews
        street['risk_score'] = len(relatedNews.keys())
    
    return street