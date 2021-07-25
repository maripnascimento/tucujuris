from flask import Flask, render_template, request
import requests


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

@app.route('/row/<number_id>', methods=['get'])	
def row_value(number_id):
	return get_lawsuit(number_id)

def get_lawsuit(lawsuit_number):
	params = {
	'id':'',
	'numero_unico': lawsuit_number,
	'captcha':''
	}
	
	print('fazendo requisicao cabecalho processo')
	
	site = requests.get("http://tucujuris.tjap.jus.br/api/publico/buscar-autos-consulta-publica",params=params,verify=False)
	data = site.json()
	
	if not data['dados']['autos']:
		return 
	
	
	params_lawsuit = {
	'autos_id': data['dados']['autos'][0]['id'],
	'chave_consumo':''
	}
	
	print('fazendo requisicao com ID processo')

	response = requests.get('http://tucujuris.tjap.jus.br/api/publico/buscar-detalhes-autos-consulta-publica',params_lawsuit)
	
	response_json = response.json()
	lawsuit = parser(response_json)

	return lawsuit

def parser(data):
	related_people = get_related_people(data['dados']['capa'])
	activity_list = get_activity_list(data['dados']['movimentos'])
	basic_info = get_basic_info(data['dados']['cabecalho'])
	
	lawsuit = {
	'basic_info':basic_info,
	'related_people': related_people,
	'activity_list': activity_list
	}

	return lawsuit

def get_related_people(data):

	print('extraindo partes do processo')

	related_people = []
	for people in data:
		part = {
		'name':people['nomeparte'],
		'role':people['tipoparte'],
		'lawyer':people['nome_adv']
		}
		related_people.append(part)

	return related_people

def get_activity_list(data):

	print('extraindo os andamentos do processo')

	activity_list = []
	for activity in data:
		moviment = {
		'title':activity['descricao_pa'],
		'text':activity['complemento_pa'],
		'date':activity['dt_andamento_pa']
		}
		activity_list.append(moviment)
	
	return activity_list

def get_basic_info(data):	

	#import pdb; pdb.set_trace()

	print ('extraindo cabecalho')

	basic_info = {
	'degree': data['instancia'],
	'number':data['numero_cnj'],
	'class':data['classe'],
	'kind':data['rito'],
	'city':data['comarca'],
	'subject':data['cnj_assunto'],
	'value':data['valor_causa'],
	'date':data['dt_distribuicao'],
	'court_section':data['lotacao']
	}

	return basic_info
	

if __name__ == '__main__':
	app.run()	

