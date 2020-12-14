import requests
import json
import sqlite3
import os
import csv
import  matplotlib
import matplotlib.pyplot as plt
import numpy as np

def visualize():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + "/main_database.db")
    cur = conn.cursor()
    
    #makes a graph of amzn value over time
    amazonList = list(cur.execute("SELECT AmazonNumbers.high FROM AmazonNumbers WHERE date % 4 = 0"))
    amazonDates = list(cur.execute("SELECT AmazonNumbers.date FROM AmazonNumbers WHERE date % 4 = 0"))
    plt.scatter(amazonDates, amazonList, s=30, c="orange")
    plt.title("Amazon Value over Time")
    plt.xlabel("Date (YYYYMMDD)")
    plt.ylabel("Amazon Single Share Value")
    plt.show()

    #makes a graph of zoom value over time
    zoomList = list(cur.execute("SELECT ZoomNumbers.high FROM ZoomNumbers WHERE date % 4 = 0")) 
    zoomDates = list(cur.execute("SELECT ZoomNumbers.date FROM ZoomNumbers WHERE date % 4 = 0")) 
    plt.scatter(zoomDates, zoomList, s=30, c="blue")
    plt.title("Zoom Value over Time")
    plt.xlabel("Date (YYYYMMDD)")
    plt.ylabel("Zoom Single Share Value")
    plt.show()



    #makes a graph of total covid cases over time
    covidList = list(cur.execute("SELECT CovidData.positive FROM CovidData WHERE date % 4 = 0"))[:76]
    newList = []
    newDays = []
    covidDates = list(cur.execute("SELECT CovidData.date FROM CovidData WHERE date % 4 = 0"))[:76]
    for pos in covidList:
        pos = pos[0]
        newList.append(str(pos))
    for day in covidDates:
        day = day[0]
        day = str(day)[5:]
        newDays.append(str(day))
    plt.scatter(newDays, newList, s=30, c="red")
    plt.title("Increase in Total Positive COVID Tests")
    plt.xlabel("Date (MMDD)")
    plt.ylabel("Total US Positive Tests to Date")
    plt.show()

    
    #bonus
    newCaseList = []
    old = 0
    for i in newList:
        if len(newCaseList) == 0: 
            newCaseList.append(0)
            old = int(i)
        else:
            new = old - int(i)
            newCaseList.append(new)
            old = int(i)
    plt.scatter(newDays, newCaseList, s=30, c="red")
    plt.title("Total New Cases Per Four Day Interval")
    plt.xlabel("DATE (MMDD)")
    plt.ylabel("New Cases Per Four Days")
    plt.show()

visualize()