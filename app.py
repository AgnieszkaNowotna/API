from flask import Flask, request, render_template

from lib import save_to_csv,load_currencies, load_values

rates = load_currencies()
offer = load_values(rates)
save_to_csv("currencies.csv", offer)

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
