import random
import pprint


departements = {1: 'CEMED',
				2: 'Departamento de Línguas e Culturas',
				3: 'Escola Superior de Saúde',
				4: 'Departamento de Electrónica, Telecomunicações e Informática',
				5: 'CIFOP',
				6: 'Serviços de Acção Social',
				7: 'Departamento de Ambiente e Ordenamento',
				8: 'Departamento de Biologia',
				9: 'Departamento de Engenharia Cerâmica e do Vidro',
				10: 'Departamento de Economia, Gestão, Engenharia Industrial e Turismo',
				11: 'Departamento de Matemática',
				12: 'Secção Autónoma de Ciências Sociais, Jurídicas e Políticas',
				13: 'Departamento de Física',
				14: 'Laboratório Central de Análises',
				15: 'Departamento de Química',
				16: 'Departamento de Geociências',
				17: 'Biblioteca',
				18: 'Departamento de Ciências da Educação',
				19: 'IT',
				20: 'IEETA',
				21: 'Departamento de Comunicação e Arte',
				22: 'Departamento de Engenharia Mecânica',
				23: 'Complexo Pedagógico, Científico e Tecnológico',
				24: 'Livraria e Sala de Exposições',
				25: 'Reitoria',
				26: 'Departamento de Biologia',
				27: 'Centro de Computação',
				28: 'Secção Autónoma de Engenharia Civil',
				29: 'Complexo de Laboratórios Tecnológicos'
				}


def generator():
	data = []
	for number in departements:
		departement = {'id': number, 'name': departements[number]}
		switches = []
		unity = ''.join([c for c in departements[number] if c.isupper()])
		unity = unity.lower()
		for s in range(1,random.randint(10, 20)):
			bastiao = random.randint(1, 3)
			if s < 10:
				identifier = unity+'-b0'+str(bastiao)+'-sw0'+str(s)+'.ua.pt'
			else:
				identifier = unity+'-b0'+str(bastiao)+'-sw'+str(s)+'.ua.pt'
			switches.append({'id': identifier, 'modelo': 'NA'})
		if number == 4:
			switches.append({'id': 'detiLab-b01-sw01.ua.pt', 'modelo': 'NA'})
			switches.append({'id': 'detiLab-b01-sw02.ua.pt', 'modelo': 'NA'})
			switches.append({'id': 'detiLab-b02-sw01.ua.pt', 'modelo': 'NA'})
		departement['switches'] = switches
		data.append(departement)
	return data


def main():
	data = generator()
	pprint.pprint(data)
	with open('data.txt', 'w') as outfile:
		outfile.write(str({'data': data}))


if __name__ == '__main__':
	main()
