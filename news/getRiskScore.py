'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

getNewsData(street,noOfDays): Returns risk_score and metadata of news articles/tags for specified noOfDays for a single street name
    risk_score: Score calculated by sum of articles returned
    risk_metadata: Dict of links to news articles and related tag

'''

#Returns news data for the last few days for a street on specified news URL
import config
import datetime, requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict

def getMilanoToday(street,startDate,endDate):
    newsUrlData = defaultdict(list)
    url = config.newsSource["MilanoToday"]+"/search/query/"+street['name'].replace(' ','+')+"/from/"+startDate+"/to/"+endDate
    response = requests.get(url)
    
    soup = BS(response.text,'html.parser')

    for article in soup.findAll('article', attrs={'data-channel':'/notizie/'}):
        for div in article.findAll('div', attrs={'class':'c-story__content'}):
            for listitem in div.findAll('ul'):
                for li in listitem.findAll('li'):
                    tagValue = li.find('a')['href'].replace('/tag/','')[:-1]
                    #Check if only the news with interested tags are taken into consideration
                    if tagValue.lower() in config.trackingTags:
                        newsUrlData[config.newsSource["MilanoToday"]+div.find('header').find('a')['href']].append(tagValue)

    return newsUrlData

def getNewsData(street,noOfDays):
    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.datetime.now() - datetime.timedelta(days = noOfDays)).strftime("%Y-%m-%d") #timedelta specified to 30 days

    relatedNews = {}

    for source in config.newsSource.keys():
        processFunction = globals()["get"+str(source)]
        for key,value in processFunction(street,startDate,endDate).items():
            relatedNews[key] = value

    if len(relatedNews.keys()) > 0:
        street['risk_metadata'] = relatedNews
        street['risk_score'] = len(relatedNews.keys()) #Calculate score based on number of articles - need to define better
    
    return street