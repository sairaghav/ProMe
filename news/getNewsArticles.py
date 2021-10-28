'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

getNewsData(street,startDate,endDate): Returns news articles/tags between specified startDate and endDate for a single street name
    Return Format: {"article_link": ["tag1","tag2"...]}

getMilanoToday(street,startDate,endDate): Scraps the search results for MilanoToday between the specified dates on the street and 
                                          returns dict with links of articles tagged with the tags specified in config.py
    Return Format: {"article_link": ["tag1","tag2"...]}
'''

import config
import requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict

def getMilanoToday(street,startDate,endDate):
    newsData = defaultdict(list)
    
    #Configure URL for MilanoToday
    url = config.newsSource["MilanoToday"]+"/search/query/"+street['name'].replace(' ','+')+"/from/"+startDate+"/to/"+endDate
    response = requests.get(url)
    lastPage = 1
    
    soup = BS(response.text,'html.parser')
    #Get total number of pages of results
    for pageItem in soup.findAll('div',attrs={'class':'c-pagination'}):
        lastPage = int(pageItem.find_all('a')[-1]['href'].split('/')[-1])
    
    #Get data from all pages of results
    for i in range(1,lastPage+1):
        url = config.newsSource["MilanoToday"]+"/search/query/"+street['name'].replace(' ','+')+"/from/"+startDate+"/to/"+endDate+"/pag/"+str(i)
        response = requests.get(url)
        soup = BS(response.text,'html.parser')

        for article in soup.findAll('article', attrs={'data-channel':'/notizie/'}):
            for div in article.findAll('div', attrs={'class':'c-story__content'}):
                for listitem in div.findAll('ul'):
                    for li in listitem.findAll('li'):
                        try:
                            tagValue = li.find('a')['href'].replace('/tag/','')[:-1]
                            #Consider only the news with interested tags
                            if tagValue.lower() in config.trackingTags:
                                newsData[config.newsSource["MilanoToday"]+div.find('header').find('a')['href']].append(tagValue)
                        except TypeError:
                            break

    return newsData
    
#Returns news data for the last few days for a street on specified news URL
def getNewsData(street,startDate,endDate):
    relatedNews = {}

    for source in config.newsSource.keys():
        processFunction = globals()["get"+str(source)]
        for key,value in processFunction(street,startDate,endDate).items():
            relatedNews[key] = value

    return relatedNews