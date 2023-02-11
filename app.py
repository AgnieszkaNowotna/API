import json
import csv
import requests
from flask import Flask

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]["rates"]

currency_list = []
code_list = []
bid_list = []
ask_list = []

for position in rates:
    currency_list.append(position['currency'])
    code_list.append(position['code'])
    bid_list.append(position['bid'])
    ask_list.append(position['ask'])


with open('currencies.csv','w',newline='',encoding="utf-8") as csvfile:
    fieldnames=["currency","code","bid","ask"]
    writer = csv.DictWriter(csvfile, delimiter =";", fieldnames = fieldnames)
    writer.writeheader()

    for i in range (len(currency_list)):
        currency = currency_list[i]
        code = code_list[i]
        bid = bid_list[i]
        ask = ask_list[i]
        writer.writerow({"currency":currency,"code":code,"bid":bid,"ask":ask})

