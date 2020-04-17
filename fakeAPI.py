import random
import pprint


departements = {1: ['UNAVE', 'UNAVE'],
				2: ['Departamento de Línguas e Culturas', ''],
				3: ['Antiga Reitoria', 'CONFUCIO'],
				4: ['Departamento de Electrónica, Telecomunicações e Informática', 'DETI'],
				5: ['Departamento de Educação e Psicologia', ''],
				6: ['Serviços de Ação Social', 'SASUA'],
				7: ['Departamento de Ambiente e Ordenamento', ''],
				8: ['Departamento de Biologia', ''],
				9: ['Departamento de Engenharia de Materiais e Cerâmica', ''],
				10: ['Departamento de Economia, Gestão e Engenharia Industrial e Turismo', 'DEGEIT'],
				11: ['Departamento de Matemática', 'DMAT'],
				12: ['Departamento de Ciências Sociais, Políticas e do Território', ''],
				13: ['Departamento de Física', ''],
				14: ['Laboratório Central de Análises', ''],
				15: ['Departamento de Química', ''],
				16: ['Departamento de Geociências', ''],
				17: ['Biblioteca', ''],
				18: ['Departamento de Ciências da Educação', ''],
				19: ['Instituto de Telecomunicações', 'IT'],
				20: ['Instituto de Engenharia Electrónica e Telemática de Aveiro', 'IEETA'],
				21: ['Departamento de Comunicação e Arte', ''],
				22: ['Departamento de Engenharia Mecânica', ''],
				23: ['Complexo Pedagógico, Científico e Tecnológico', ''],
				24: ['Livraria e Sala de Exposições', ''],
				25: ['Reitoria', ''],
				26: ['Departamento de Biologia', ''],
				27: ['Serviços de Tecnologias de Informação e Comunicação', ''],
				28: ['Departamento de Engenharia Civil', ''],
				29: ['Complexo de Laboratórios Tecnológicos', ''],
				'A': ['Instituto Superior de Contabilidade e Administração', 'ISCA'],
				'B': ['Residências de Estudantes', ''],
				'C': ['Residência de Docentes, Funcionários e Estudantes de Pós-graduação', ''],
				'D': ['Instituto de Ambiente e Desenvolvimento', 'IDAD'],
				'E': ['Pavilhão Polidesportivo Prof. Dr. Aristides Hall', ''],
				'F': ['Restaurante Universitário', ''],
				'G': ['Creche e Jardim Infantil', ''],
				'H': ['Centro de Estudos do Ambiente e do Mar', 'CESAM'],
				'I': ['Grupo Experimental do Teatro da UA', 'GRETUA'],
				'M': ['Complexo de Refeitórios do Crasto', ''],
				'N': ['Casa do Estudante', 'AAUAv'],
				'O': ['Estação Meteorológica', '']
				}


models = ['cisco WS-C2950T-24', 'cisco WS-C2950T-48-SI']


def generator():
	data = []
	for number in departements:
		acron_dep = departements[number][1]
		departement = {'id_dep': number, 'name_dep': departements[number][0], 'acron_dep': acron_dep}
		switches = []
		for s in range(1,random.randint(10, 20)):
			bastiao = random.randint(1, 3)
			if s < 10:
				identifier = acron_dep.lower()+'-b0'+str(bastiao)+'-sw0'+str(s)+'.ua.pt'
			else:
				identifier = acron_dep.lower()+'-b0'+str(bastiao)+'-sw'+str(s)+'.ua.pt'
			switches.append({'identifier_switch': identifier, 'model_switch': models[random.randint(0, 1)]})
		if number == 4:
			switches.append({'identifier_switch': 'detiLab-b01-sw01.ua.pt', 'model_switch': 'cisco WS-C2950T-24'})
			switches.append({'identifier_switch': 'detiLab-b01-sw02.ua.pt', 'model_switch': 'cisco WS-C2950T-48-SI'})
			switches.append({'identifier_switch': 'detiLab-b02-sw01.ua.pt', 'model_switch': 'cisco WS-C2950T-24'})
		departement['switches'] = switches
		data.append(departement)
	return data


def main():
	data = generator()
	pprint.pprint(data)
	with open('data.txt', 'w') as outfile:
		outfile.write(str(data))


if __name__ == '__main__':
	main()
