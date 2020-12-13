import requests
import json
import sqlite3
import os
import csv

#setting up covid api and printing covid data
def covidapi():
    url = 'https://api.covidtracking.com'
    dataset_key = '/v1/us/daily.json'
    jsoncoviddata = requests.get(url + dataset_key)
    totalcases = {}
    for day in jsoncoviddata.json():
        totalcases[day['date']] = day['positive']
        highestcases = sorted(totalcases.items(), reverse = True)
    return highestcases

def zoomapi():
    # make the http GET request to IEX data for the last year of Zoom stock
    zoom_data = requests.get('https://sandbox.iexapis.com/stable/stock/ZM/chart/12m?token=Tpk_3887575474904b80ac60139ecc2100b1')

    # the JSON response from IEX API, data includes dates in YEAR-MM-DD format under "date", 948 items
    #print(json.dumps(zoom_data.json()))
    z_date_data = {}
    for line in zoom_data.json():
        date = str(line["date"])
        amount = float(line["high"])
        z_date_data[date] = amount
        highest_z = sorted(z_date_data.items(), reverse = True)
    return highest_z
    

def amazonapi():
    # make the http GET request to Alphavantage data for monthly Amazon stock data
    
    data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AMZN&apikey=9T46ONZRXIT0CDFW')
    amazon_data = data.json()
    # the JSON response from AV API, data includes dates in YEAR-MM-DD format as title of dictionary, 419 items
    #print(amazon_data["Monthly Time Series"])

    a_date_data = {}
    dates = amazon_data["Time Series (Daily)"]
    for date in dates.keys():
        highest = dates[date]['2. high']
        a_date_data[date] = float(highest)
        highest_a = sorted(a_date_data.items(), reverse = True)
    return highest_a


def covid_database():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + "/main_database.db")
    cur = conn.cursor()
    
    necessary_info = cur.execute("DROP TABLE IF EXISTS CovidData")
    cur.execute("CREATE TABLE CovidData (date INTEGER PRIMARY KEY, positive TEXT)")
    covid_lst = []
    for i in necessary_info:
        covid_lst.append(i[0])
    count = 0
    day_data = covidapi()
    line = 'INSERT OR IGNORE INTO CovidData (date, positive) VALUES (?, ?)'
    for day in day_data:
        if count == 25:
            break
        if day[0] in day_data:
            continue
        else:
            cur.execute(line, (day[0], day[1]))
            count += 1
    conn.commit()
    conn.close()


def zoom_database():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + "/main_database.db")
    cur = conn.cursor()
    necessary_info = cur.execute("DROP TABLE IF EXISTS ZoomNumbers")
    cur.execute("CREATE TABLE ZoomNumbers (date TEXT, high FLOAT)")
    zoom_lst = []
    for i in necessary_info:
        zoom_lst.append(i[0])
    count = 0
    day_data = zoomapi()
    line = 'INSERT OR IGNORE INTO ZoomNumbers (date, high) VALUES (?, ?)'
    for day in day_data:
        if count == 25:
            break
        if day[0] in day_data:
            continue
        else:
            cur.execute(line, (day[0].replace("-", ""), day[1]))
            count += 1
    conn.commit()
    conn.close()
    

def amazon_database():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + "/main_database.db")
    cur = conn.cursor()
    necessary_info = cur.execute("DROP TABLE IF EXISTS AmazonNumbers")
    cur.execute("CREATE TABLE AmazonNumbers (date TEXT, high FLOAT)")
    amazon_lst = []
    for i in necessary_info:
        amazon_lst.append(i[0])
    count = 0
    day_data = amazonapi()
    line = 'INSERT OR IGNORE INTO AmazonNumbers (date, high) VALUES (?, ?)'
    for day in day_data:
        if count == 25:
            break
        if day[0] in day_data:
            continue
        else:
            cur.execute(line, (day[0].replace("-", ""), day[1]))
            count += 1
    conn.commit()
    conn.close()


covidapi()
zoomapi()
amazonapi()
covid_database()
zoom_database()
amazon_database()