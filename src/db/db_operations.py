import sqlite3, datetime
from news import news_articles
import config

path = 'src/db/'
db_name = 'streets.db'

con = sqlite3.connect(path+db_name, check_same_thread=False)
cur = con.cursor()

def init_tables():
    cur.execute('CREATE TABLE IF NOT EXISTS street_list (last_update_time text, street text, risk_score text)')
    con.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS street_news (date text, time text, source text, street text, tags text, link text)')
    con.commit()

def insert_street_data(street: str) -> None:
    cur = con.cursor()
    table_name = 'street_list'
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute('INSERT INTO '+table_name+' values (?,?)', ( 
                str(update_time),
                str(street)
            )
    )

    con.commit()

def update_street_data(street: str) -> None:
    table_name = 'street_list'
    
    cur.execute('DELETE FROM '+table_name+' WHERE street=:street', {"street": street})
    con.commit()

    insert_street_data(street)

def insert_street_risk_data(news_data: dict) -> None:
    table_name = 'street_news'

    cur.execute('INSERT INTO '+table_name+' VALUES (?,?,?,?,?,?)', (
                str(news_data['date']),
                str(news_data['time']),
                str(news_data['source']),
                str(news_data['street']),
                str(news_data['tags']),
                str(news_data['link']),
                )
    )
    con.commit()

def update_street_risk_data(news_data: dict) -> None:
    table_name = 'street_news'
    
    cur.execute('DELETE FROM '+table_name+' WHERE street=:street', {"street": news_data['street']})
    con.commit()

    insert_street_risk_data(news_data)

def search_street_data(street: str) -> tuple:
    table_name = 'street_list'
    cur.execute('SELECT * FROM '+table_name+' WHERE street=:street', {"street": street})
    return cur.fetchall()

def search_street_risk_data(street: str) -> list[dict]:
    table_name = 'street_news'

    cur.execute('SELECT * FROM '+table_name+' WHERE street=:street', {"street": street})
    output = cur.fetchall()

    results = []
    result = {}

    columns = list(map(lambda x: x[0], cur.description))

    for row in output:
        for column in columns:
            result[column] = row[columns.index(column)]
        results.append(result.copy())

    return results


def check_last_updated_time(street: str):
    if len(search_street_data(street)) > 0:
        time_difference = datetime.datetime.now() - datetime.datetime.strptime(search_street_data(street)[0][0],"%Y-%m-%d %H:%M:%S")
        return time_difference

    else: 
        return None
        
def get_news_data(street_name: str, 
                  from_date=(datetime.datetime.now() - datetime.timedelta(days=config.fetch_news_for_interval_days)).strftime("%Y-%m-%d"), 
                  to_date=(datetime.datetime.now().strftime("%Y-%m-%d"))
                ) -> list:
    last_checked_time = check_last_updated_time(street_name)
    result = []

    if last_checked_time is None:
        for street_news in news_articles.fetch_from_all_sources(street_name, from_date, to_date):
            insert_street_risk_data(street_news._asdict())
            result.append(street_news._asdict())
        insert_street_data(street_name)

    elif last_checked_time.seconds > 24*60*60:
        for street_news in news_articles.fetch_from_all_sources(street_name, from_date, to_date):
            update_street_risk_data(street_news._asdict())
            result.append(street_news._asdict())
        update_street_data(street_name)

    else:
        for street_news in search_street_risk_data(street_name):
            result.append(street_news)

    return result

def get_risk_score(street: dict)-> dict:
    result = get_news_data(street['name'])
    
    street['risk_metadata'] = result
    street['risk_score'] = len(result)

    return street