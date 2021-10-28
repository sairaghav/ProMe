import csv, datetime, requests
from urllib.parse import quote as url_encode
from typing import NamedTuple
import os.path as path

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

baseUrl = "http://localhost:5000/news"

endDate = datetime.datetime.now().strftime("%Y-%m-%d")
startDate = "2018-01-01"  # (datetime.datetime.now() - datetime.timedelta(days = 730)).strftime("%Y-%m-%d")


class NewsDataRow(NamedTuple):
    date: str
    time: str
    source: str
    street: str
    tags: str
    link: str


csv_path = path.join(path.dirname(path.realpath(__file__)), "..", "datasets", f"NewsData_{startDate}_{endDate}.csv")
with open(csv_path, 'w+', encoding='UTF8', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow([field.capitalize() for field in NewsDataRow._fields])
    for ind, street in enumerate(streets):
        finalUrl = f"{baseUrl}/{url_encode(street)}/{url_encode(startDate)}/{url_encode(endDate)}"
        print(f"Processing: {street} ({ind + 1} / {len(streets)})", end="\r")
        response = requests.get(finalUrl)
        parsed_response = response.json()
        writer.writerows([NewsDataRow(**row) for row in parsed_response[street]])
        print(" " * 80, end="\r")
print("OK, wrote CSV:")
print(path.realpath(csv_path))
