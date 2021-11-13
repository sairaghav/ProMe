import os

from news.parsers import MilanoToday

trackingTags = ['furti', 'droga', 'arresti', 'incidenti', 'rapine', 'vandali', 'incidenti-stradali', 'aggressioni',
                'indagini', 'morti']  # Will hold exhaustive collection of all tags to check

mapBaseUrl = "http://open.mapquestapi.com"
mapApiKey = os.environ.get("MAPS_API_KEY", None)
if not mapApiKey:
    raise ValueError("""
    Missing API Key, please provide it via `export MAPS_API_KEY=<key>` on the shell before running the code
    Hint: Check out the Telegram group for it ;)
    """)

sources = [MilanoToday]
# Other news sources can be added in news/parsers/ directory.
fetch_news_for_interval_days = 14

significant_place_types = ["hospitals", "police", "bus", "metro", "tram"]
