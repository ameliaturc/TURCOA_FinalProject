import requests
import json
import sqlite3
import os
import csv
import  matplotlib
import matplotlib.pyplot as plt
import numpy as np

def calculations():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + "/main_database.db")
    cur = conn.cursor()
    covidstart = cur.execute("SELECT MAX(positive) FROM CovidData WHERE date = 20200723")
    covid1 = int(list(covidstart)[0][0])
    covidend = cur.execute("SELECT MAX(positive) FROM CovidData WHERE date = 20201211")
    increase = int(list(covidend)[0][0]) - covid1
    startstocks = cur.execute("SELECT AmazonNumbers.high, ZoomNumbers.high FROM AmazonNumbers JOIN ZoomNumbers ON AmazonNumbers.date = ZoomNumbers.date WHERE AmazonNumbers.date AND ZoomNumbers.date = 20200724") #20200723
    stocksinitial = list(startstocks)
    amzstart = stocksinitial[0][0]
    zoomstart = stocksinitial[0][-1]
    endstocks = cur.execute("SELECT AmazonNumbers.high, ZoomNumbers.high FROM AmazonNumbers JOIN ZoomNumbers ON AmazonNumbers.date = ZoomNumbers.date WHERE AmazonNumbers.date AND ZoomNumbers.date = 20201211")
    stocksfinal = list(endstocks)
    amzincrease = stocksfinal[0][0] / amzstart
    zoomincrease = stocksfinal[0][-1] / zoomstart

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/calculations.csv", "w") as calculations:
        calcwriter = csv.writer(calculations)
        calcwriter.writerow(["Increase in Covid Cases from July 24th to December 11th", increase])
        calcwriter.writerow(["Increase in Amazon Stock Price from July 24th to December 11th", amzincrease])
        calcwriter.writerow(["Increase in Zoom Stock Price from July 24th to December 11th", zoomincrease])

calculations()