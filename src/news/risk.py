'''
Author: Sairaghav (https://github.com/sairaghav)

Description: Returns risk_score and risk_metadata for input street calculated by scraping news articles and tags

calcRiskScore(street): Returns risk_score and metadata of news articles/tags for a single street name
    risk_score: Score calculated by sum of articles returned
    risk_metadata: Dict of links to news articles and related tag

'''

import config
import datetime

from . import news_articles


# Returns news data for the last few days for a street on specified news URL
def calculate_score(street):
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime(
        "%Y-%m-%d")  # timedelta taken from config.py

    news_results = []
    for related_news in news_articles.fetch_from_all_sources(street['name'], start_date, end_date):
        news_results.append(related_news._asdict())
    
    street['risk_metadata'] = news_results
    street['risk_score'] = len(news_results)  # Calculate score based on number of articles - need to define better

    
    return street
