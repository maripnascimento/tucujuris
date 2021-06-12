from flask import Flask, render_template, request
import requests

from .crawler import get_lawsuit

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	number = request.form['number']
	return get_lawsuit(number)

if __name__ == '__main__':
	app.run()	

