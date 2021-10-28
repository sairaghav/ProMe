'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

calcRiskScore(street): Returns risk_score and metadata of news articles/tags for a single street name
    risk_score: Score calculated by sum of articles returned
    risk_metadata: Dict of links to news articles and related tag

'''

import config
import datetime, requests
from bs4 import BeautifulSoup as BS
from collections import defaultdict

from . import getNewsArticles
 
#Returns news data for the last few days for a street on specified news URL
def calcRiskScore(street):
    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.datetime.now() - datetime.timedelta(days = config.newsNoOfDays)).strftime("%Y-%m-%d") #timedelta taken from config.py

    relatedNews = {}
    relatedNews = getNewsArticles.getNewsData(street,startDate,endDate)

    if len(relatedNews) > 0:
        street['risk_metadata'] = relatedNews
        street['risk_score'] = len(relatedNews) #Calculate score based on number of articles - need to define better
    
    return street