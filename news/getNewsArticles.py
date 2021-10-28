'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

getNewsData(street,startDate,endDate): Returns news articles/tags between specified startDate and endDate for a single street name

    Input:
        street (dict): 
            street['name'] = string

        startDate (string): yyyy-mm-dd
        endDate (string): yyyy-mm-dd

    Returns:
        relatedNews (list of dict):
            news['street']: Name of street
            news['source]: Source of news
            news['tags']: Associated tags
            news['link']: Link for news article
            news['date']: Date of news article
            news['time']: Time of news article


getMilanoToday(street,startDate,endDate): Scraps the search results for MilanoToday between the specified dates on the street and 
                                          returns dict with links of articles tagged with the tags specified in config.py
    
    Input:
        street (dict): 
            street['name'] = string

        startDate (string): yyyy-mm-dd
        endDate (string): yyyy-mm-dd

    Returns:
        relatedNews (list of dict):
            news['street']: Name of street
            news['source]: Source of news
            news['tags']: Associated tags
            news['link']: Link for news article
            news['date']: Date of news article
            news['time']: Time of news article
'''

import config
import requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict

def getMilanoToday(street,startDate,endDate):
    news = defaultdict(list)
    newsData = {}
    allData = []
    
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
                            #Consider only the news     with interested tags
                            if tagValue.lower() in config.trackingTags:
                                news[config.newsSource["MilanoToday"]+div.find('header').find('a')['href']].append(tagValue)
                        except TypeError:
                            break

    #Data enrichment for news article data
    for link in news.keys():
        newsData['source'] = "MilanoToday"
        newsData['link'] = link
        newsData['tags'] = ','.join(set(news[link]))
        newsData['street'] = street['name']

        response = requests.get(link)
        soup = BS(response.text,'html.parser')

        timestamp = soup.find('span',attrs={'data-timestamp':True}).contents[0]
        
        newsData['date'] = ' '.join(timestamp.split(' ')[:3])
        newsData['time'] = timestamp.split(' ')[3]

        allData.append(newsData.copy())

    return allData
    
#Returns news data for the last few days for a street on specified news URL
def getNewsData(street,startDate,endDate):
    for source in config.newsSource.keys():
        processFunction = globals()["get"+str(source)]
        relatedNews = processFunction(street,startDate,endDate)

    return relatedNews