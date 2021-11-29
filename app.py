from flask import Flask, render_template, request
import requests
from tucujuris.crawler.crawler_tucujuris import get_lawsuit


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	number = request.form['number']
	lawsuit = get_lawsuit(number)
	if not lawsuit:
		return render_template('notfound.html')

	return render_template('result.html',lawsuit=lawsuit)

@app.route('/raw/<number_id>', methods=['get'])	
def raw_value(number_id):
	return get_lawsuit(number_id)


	
if __name__ == '__main__':
	app.run()	

