import csv, datetime, requests, json

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
startDate = "2018-01-01"#(datetime.datetime.now() - datetime.timedelta(days = 730)).strftime("%Y-%m-%d")

with open('../datasets/NewsData_'+startDate+'_'+endDate+'.csv', 'w+', encoding='UTF8', newline='') as f:
    for street in streets:
        finalUrl = baseUrl+"/"+street.replace(' ','%20')+"/"+startDate+"/"+endDate
        print(finalUrl)
        response = requests.get(finalUrl)
        responseData = json.loads(response.text)

        writer = csv.writer(f)
        writer.writerow(["Date","Time","Source","Street","Tags","Link"])
        for data in responseData[street]:
            writer.writerow([data['date'],data['time'],data['source'],data['street'],data['tags'],data['link']])
