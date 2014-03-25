from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib

app = Flask(__name__)

text = urllib.urlopen("http://www.vincentmetals.com/1Pricing/Price_Data/")
soup = BeautifulSoup(text)
table = soup.find("table")
price_cell = table.findAll('td')[9:16]

def whole_shebang(list):
	prices = []
	metals = ["aluminum", "copper", "gold", "nickel", "platinum", "silver", "zinc"]
	for i in list:
		i = "%r" % i

		i = i.strip('<td class="priceCell2" valign="top">')
		i = i.strip('1" valign="top">')
		i = i.strip('</')
		i = float(i)
		if len(str(i)) >= 5:
			prices.append(i+1000.0)
		else:
			prices.append(i)

	dictionary = dict(zip(metals, prices))
	dictionary['silver'] = dictionary['silver'] - 1000
	dictionary['gold'] = dictionary['gold']*16
	dictionary['silver'] = dictionary['silver']*16
	dictionary['platinum'] = dictionary['platinum']*16

	for mineral in dictionary:
		if mineral == 'gold':
			mineral = 0

	return dictionary

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		metal = request.form['metal']
		pounds = request.form['pounds']
		ounces = request.form['ounces']
		
		weight = get_weight(pounds, ounces)
		
		value = value_of_metal(metal, weight)
		return metal, ounces, pounds
	else:
		metal = ''
		pounds = 1
		ounces = 1
		value = 10 
		
	return render_template('index.html', metal=metal, pounds=pounds, ounces=ounces)
	index.methods = ['POST']


@app.route('/prices', methods=['GET', 'POST'])
def prices():

	price_dict = whole_shebang(price_cell) # this should bring all that in
	if request.method == "POST":
		metal = request.form['metal']
		if metal in price_dict:
			price = price_dict[metal]
		pounds = float(request.form['pounds'])
		ounces = float(request.form['ounces'])/16.0
		weight = pounds + ounces
		value = price * weight

		

		return render_template('index.html', metal=metal, pounds=pounds, ounces=ounces, price=price, weight=weight, value = value)

	else:
		return "Whaaaat?"



if __name__ =="__main__":
	app.debug = True
	app.run()

