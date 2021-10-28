import os

trackingTags = ['furti','droga','arresti','incidenti','rapine','vandali','incidenti-stradali','aggressioni','indagini','morti'] #Will hold exhaustive collection of all tags to check

mapBaseUrl = "http://open.mapquestapi.com"
mapApiKey = os.environ['MAPS_API_KEY']

newsSource = {"MilanoToday": "https://www.milanotoday.it"} #Other news sources can be added in the same format. If news source is added, specify
                                                            #function with format `get{$source}` in news/getNewsArticles.py
newsNoOfDays = 14 #No. of days to search news for

placesOfInterest = ["hospitals", "police", "bus", "metro","tram"]

