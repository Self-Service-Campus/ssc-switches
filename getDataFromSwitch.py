import logging
import argparse
import pprint
from SwitchConnector import SwitchConnector 


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("root")
USERNAME = 'root'
PASSWORD = 'DETi4sw'


def getPorts(switch, data):
	ports = []
	for d in data:
		port = {}
		port['id_port'] = switch.replace('.ua.pt', '_' + d['Port'])
		port['number_port'] =  d['Port']
		if d['Name'] != '':
			port['name_port'] = d['Name'].replace(' (','')
		port['state_port'] = d['Status']
		ports.append(port)
	return ports


def main(switches):
	returnData = []
	for switch_IP in switches:
		connector = SwitchConnector(LOGGER, USERNAME, PASSWORD, switch_IP, 'show version')
		data = connector.run()
		switch = {'id_switch': switch_IP.replace('.ua.pt', ''), 'ip_switch': switch_IP, 'model_switch': data['Model number']}
		connector.setCommand('show interfaces status')
		data = connector.run()
		ports = {}
		ports['switch'] = switch
		ports['ports'] = getPorts(switch_IP, data)
		returnData.append(ports)
	pprint.pprint(returnData)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--switches", nargs='+', default=[], help="Switches IP address", required=False)
	args = parser.parse_args()
	main(args.switches)
