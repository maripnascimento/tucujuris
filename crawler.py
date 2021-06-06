import requests

def get_lawsuit(lawsuit_number):
	params = {
	'id':'',
	'numero_unico': lawsuit_number,
	'captcha':'nada'
	}
	
	print('fazendo requisicao cabecalho processo')
	
	site = requests.get("http://tucujuris.tjap.jus.br/api/publico/buscar-autos-consulta-publica",params=params,verify=False)
	data = site.json()
	# import pdb; pdb.set_trace()
	if not data['dados']['autos']:
		return 'o processo nao foi encontrado'
	lawsuit_id = data['dados']['autos'][0]['id']

	
	params_lawsuit = {
	'autos_id': lawsuit_id,
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
		'nome':people['nomeparte'],
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
		'titulo':activity['descricao_pa'],
		'complemento':activity['complemento_pa'],
		'data':activity['dt_andamento_pa']
		}
		activity_list.append(moviment)
	
	return activity_list

def get_basic_info(data):	

	print ('extraindo cabecalho')

	basic_info = {
	'class':data['classe'],
	'rito':data['rito'],
	'comarca':data['comarca'],
	'assunto':data['cnj_assunto'],
	'valor_causa':data['valor_causa'],
	'distribuicao':data['dt_distribuicao'],
	'lotacao':data['lotacao']
	}

	return basic_info
	

# number = input("Qual processo vc quer consultar?") 
number = '0002120-57.2020.8.03.0001'

print (get_lawsuit(number))


# muito orgulho!
