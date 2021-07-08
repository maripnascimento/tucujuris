from flask import Flask, render_template, request
import requests

from .crawler_tucujuris import get_lawsuit

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


if __name__ == '__main__':
	app.run()	

