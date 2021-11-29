import os

from ProMeAPI.services.news.parsers import MilanoToday

trackingTags = {
                'terrorismo': 3,
                'furti': 2,
                'rapine': 2,
                'droga': 2,
                'aggressioni':2,
                'arresti': 1,
                'incidenti': 1,
                'vandali': 1,
                'incidenti-stradali': 1,
                'indagini':1,
                'morti':1
            }  # Will hold exhaustive collection of all tags to check

mapBaseUrl = "http://open.mapquestapi.com"
mapApiKey = os.environ.get("MAPS_API_KEY", None)
if not mapApiKey:
    raise ValueError("""
    Missing API Key, please provide it via `export MAPS_API_KEY=<key>` on the shell before running the code
    Hint: Check out the Telegram group for it ;)
    """)

sources = [MilanoToday]
# Other news sources can be added in news/parsers/ directory.
fetch_news_for_interval_days = 30

significant_place_types = ["hospitals", "police", "bus", "metro", "tram"]