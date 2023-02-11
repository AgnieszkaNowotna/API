import csv
import requests
from flask import Flask, request, render_template

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]["rates"]

class Currency():
    def __init__(self, currency, code, bid, ask):
        self.currency = currency
        self.code = code
        self.bid = bid
        self.ask = ask

def load_values():
    list = []
    for position in rates:
        position['currency'] = Currency(position['currency'], position['code'], position['bid'], position['ask'])
        list.append(position['currency'])
    return list
    
offer = load_values()

with open('currencies.csv','w',newline='',encoding="utf-8") as csvfile:
    fieldnames=["currency","code","bid","ask"]
    writer = csv.DictWriter(csvfile, delimiter =";", fieldnames = fieldnames)
    writer.writeheader()

    for currency in offer:
        writer.writerow({"currency":currency.currency,"code":currency.code,"bid":currency.bid,"ask":currency.ask})

app = Flask(__name__)

@app.route('/exchange', methods = ['GET','POST'])
def exchange():
    if request.method =='POST':

        code = request.form['currency']
        amount = request.form['amount']
        
        for instance in offer:
            if instance.code == code:
                cost = int(amount) * instance.ask
                text =f"Zakup {amount} {code} kosztuje {cost:.2f} PLN"
        return render_template('response.html', text=text)

    return render_template('currencies_exchange.html', offer = offer)

if __name__=='__main__':
    app.run(debug=True)
