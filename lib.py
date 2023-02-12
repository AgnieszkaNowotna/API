import requests
import csv

from models import Currency

def load_currencies():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates = data[0]["rates"]
    return rates

def load_values(rates):
    values = []
    for position in rates:
        currency = Currency(position['currency'], position['code'], position['bid'], position['ask'])
        values.append(currency)
    return values

def save_to_csv(file_name,offer):
    with open(file_name,'w',newline='',encoding="utf-8") as csvfile:
        fieldnames=["currency","code","bid","ask"]
        writer = csv.DictWriter(csvfile, delimiter =";", fieldnames = fieldnames)
        writer.writeheader()
        for currency in offer:
            writer.writerow({"currency":currency.currency,"code":currency.code,"bid":currency.bid,"ask":currency.ask})
