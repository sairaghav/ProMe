# Scripts folder

Contains all scripts to run in local environment

**generateNewsDataset.py:**
Makes an API call to /news/ endpoint and creates a CSV file in `datasets/` folder contain data from all news sources

The CSV file has following information:

- news['street']: Name of street
- news['source]: Source of news
- news['tags']: Associated tags
- news['link']: Link for news article
- news['date']: Date of news article
- news['time']: Time of news article