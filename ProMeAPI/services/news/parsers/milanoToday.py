from .classes import *
import datetime, pytz
from ... import config


class MilanoToday(AbstractNewsSource):
    _base_url = "https://www.milanotoday.it"
    name = "MilanoToday"

    @staticmethod
    def parse_news_page(soup: BeautifulSoup, partial_news: News) -> News:
        timestamp = soup.find('span', attrs={'data-timestamp': True}).contents[0]
        
        date = timestamp.split(' ')[0]+'-'+config.month_number_map[timestamp.split(' ')[1].lower()]+'-'+timestamp.split(' ')[2]+' '+timestamp.split(' ')[3]
        date = datetime.datetime.strptime(date,'%d-%m-%Y %H:%M')
        date = pytz.timezone('Europe/Rome').localize(date).astimezone(pytz.timezone('UTC'))

        return partial_news._replace(date=date)

    @staticmethod
    def parse_news_list(soup: BeautifulSoup) -> List[News]:
        result = []
        for article in soup.findAll('article', attrs={'data-channel': '/notizie/'}):

            for article_content_div in article.findAll('div', attrs={'class': 'c-story__content'}):
                title = article_content_div.find('header').find('h1').contents[0]
                print(title)
                link = article_content_div.find('header').find('a')['href']
                tags = []
                for tag_list in article_content_div.findAll('ul'):
                    for tag_element in tag_list.findAll('li'):
                        try:
                            tag = tag_element.find('a')['href'].replace('/tag/', '')[:-1]
                            tags.append(tag)
                        except TypeError:
                            break
                tag_str = ",".join(set(tags))
                news = News(source=MilanoToday.name, title=title, link=MilanoToday._base_url+link, tags=tag_str, date="", street="")
                result.append(news)
        return result

    @staticmethod
    def parse_page_ids(soup: BeautifulSoup) -> List[str]:
        last_page = 1
        for pageItem in soup.findAll('div', attrs={'class': 'c-pagination'}):
            last_page = int(pageItem.find_all('a')[-1]['href'].split('/')[-1])
        return [str(i) for i in range(1, last_page + 1)]

    @staticmethod
    def get_url(query: NewsQuery) -> str:
        url = f"{MilanoToday._base_url}/search/query/{url_encode(query.street)}/from/{url_encode(query.start_date)}/to/{url_encode(query.end_date)}"
        if query.page:
            url += f"/pag/{query.page}"
        return url
