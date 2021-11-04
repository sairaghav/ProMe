import csv
import datetime
import os.path as path

from news import news_articles
from news.parsers import News

streets = [
    "Viale Monza",
    "Piazza Duca d'Aosta",
    "Via Messina",
    "Via Paolo Sarpi",
    "Viale Pasubio",
    "Piazza 25 Aprile",
    "Viale Monte Grappa",
    "Piazza Luigi Einaudi",
    "Corso Buenos Aires",
    "Corso Giacomo Matteotti",
    "Corso Venezia",
    "Via Pisoni, Milan",
    "Via San Pietro all'Orto, Milan",
    "Viale Enrico Forlanini",
    "Via Santo Spirito, Milan",
    "Via Sant'Andrea",
    "Viale Luigi Majno",
    "Via Borgospesso, Milan",
    "Via Dante",
    "Via della Spiga",
    "Via Manzoni",
    "Via Monte Napoleone"
]

end_date = datetime.datetime.now().strftime("%Y-%m-%d")
start_date = "2018-01-01"  # (datetime.datetime.now() - datetime.timedelta(days = 730)).strftime("%Y-%m-%d")

csv_path = path.join(path.dirname(path.realpath(__file__)), "..", "datasets", f"NewsData_{start_date}_{end_date}.csv")
with open(csv_path, 'w+', encoding='UTF8', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow([field.capitalize() for field in News._fields])
    for ind, street in enumerate(streets):
        print(f"Processing: {street} ({ind + 1} / {len(streets)})", end="\r")
        results = news_articles.fetch_from_all_sources(street, start_date, end_date)
        writer.writerows(results)
        print(" " * 80, end="\r")
print("OK, wrote CSV:")
print(path.realpath(csv_path))
