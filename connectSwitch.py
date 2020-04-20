import paramiko
import pprint
import re
import time


switches = ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt']
commands_show = ['show arp', 'show interfaces status', 'show vlan']
commands_change = {'create_vlan': ['config t', 'vlan {}'],
					'change_vlan': ['config t', 'int {}', 'switchport mode access', 'switch access vlan {}']}

username = 'root'
password = 'DETi4sw'


def connectSwitchShow(switch, cmd_to_execute):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(switch, username=username, password=password, look_for_keys=False, timeout=None)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
		data = ssh_stdout.readlines()
		ssh.close()
	except Exception as e:
		return False, 'Error to connect!'
	return True, data


def connectSwitchChange(switch, cmd_to_execute, args):
	if cmd_to_execute == 'change_vlan':
		exec_c = commands_change['change_vlan']
		exec_c[1] = exec_c[1].format(args['inter'])
		exec_c[3] = exec_c[3].format(args['vlan'])
	elif cmd_to_execute == 'create_vlan':
		exec_c = commands_change['create_vlan']
		exec_c[1] = exec_c[1].format(args['vlan'])
	cmd_to_execute = exec_c

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(switch, username=username, password=password, look_for_keys=False, timeout=None)
		connection = ssh.invoke_shell()
		for c in cmd_to_execute:
			time.sleep(1)
			connection.send(c + '\n')
		ssh.close()
	except Exception as e:
		return False, 'Error to connect!'
	return True, 'Success!'


def initialData(data):
	try:
		data = data[15:]
		while data[0] == '\r\n':
			data = data[1:]
		initial_data = []
		d = []
		for x in range(0, len(data)):
			if data[x] != '\r\n':
				d.append(data[x])
			else:
				if len(d) > 0:
					initial_data.append(d)
					d = []
			if x == len(data)-1:
				if len(d) > 0:
					initial_data.append(d)
	except Exception as e:
		return False, 'Error to work initial data!'
	return True, initial_data


def workData(data):
	try:
		header = data[0]
		header = header.replace('\r', '')
		header = header.replace('\n', '')
		start_column = [0]
		for i in range(2, len(header)):
			if header[i-2] == ' ' and header[i-1] == ' ' and header[i] != ' ':
				start_column.append(i-1)
		start_column.append(0)

		split_data = []
		for i in range(0, len(data)):
			d = []
			for j in range(1, len(start_column)):
				if j == len(start_column)-1:
					k = list(filter(None, re.split(r'\s', data[i][start_column[j-1]:])))
				else:
					k = list(filter(None, re.split(r'\s', data[i][start_column[j-1]:start_column[j]])))
				if len(k) > 1:
					k = ' '.join(str(x) for x in k)
				elif len(k) == 0:
					k = ''
				else:
					k = k[0]
				d.append(k)
			split_data.append(d)

		final_data = []
		header = split_data[0]
		for i in range(1, len(split_data)):
			worked_data = {}
			for j in range(0, len(header)):
				worked_data[header[j]] = split_data[i][j]
			final_data.append(worked_data)
	except Exception as e:
		return False, 'Error to work data!'
	return True, final_data


def main():
	switch = switches[0]
	c = 'create_vlan'
	args = {'inter': 'Fa0/6', 'vlan' : '21'}
	c = commands_show[0]
	if c in commands_show:
		success, data = connectSwitchShow(switch, c)	
		if success:
			success, data = initialData(data)
			for d in data:
				success, data = workData(d)
				if success:
					pprint.pprint(data)
				else:
					print(data)
		else:
			print(data)
	else:
		success, text = connectSwitchChange(switch, c, args)
		print(text)



if __name__ == '__main__':
	main()