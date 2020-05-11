import paramiko
import re
import time

POST_COMMANDS = {'create_vlan': ['config t', 'vlan {}', 'name {}', 'end'],
                 'delete_vlan': ['config t', 'no vlan {}', 'end'],
                 'change_vlan': ['config t', 'int {}', 'switchport mode access', 'switch access vlan {}', 'end']}


def getPorts(switch, data):
    try:
        ports = []
        for d in data:
            port = {'id_port': switch.replace('.ua.pt', '') + '_' + d['Port'],
                    'number_port': d['Port'],
                    'state_port': d['Status'],
                    'vlan': d['Vlan']}
            if d['Name'] != '':
                port['name_port'] = d['Name'].split(' (')[0]
            ports.append(port)
    except Exception as e:
        return {'success': False, 'error': 'Error to get Ports!'}
    return {'success': True, 'data': ports}


def initialData(data):
    try:
        data = data[14:]
        while data[0] == '\r\n':
            data = data[1:]
        initial_data = data
    except Exception as e:
        return {'success': False, 'error': 'Error to work initial data!'}
    return {'success': True, 'data': initial_data}


def workData(data):
    try:
        header = data[0]
        header = header.replace('\r', '')
        header = header.replace('\n', '')
        start_column = [0]
        for i in range(2, len(header)):
            if header[i - 2] == ' ' and header[i - 1] == ' ' and header[i] != ' ':
                start_column.append(i - 1)
        start_column.append(0)

        split_data = []
        for i in range(0, len(data)):
            d = []
            for j in range(1, len(start_column)):
                if j == len(start_column) - 1:
                    k = list(filter(None, re.split(r'\s', data[i][start_column[j - 1]:])))
                else:
                    k = list(filter(None, re.split(r'\s', data[i][start_column[j - 1]:start_column[j]])))
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
        return {'success': False, 'error': 'Error to work data!'}
    return {'success': True, 'data': final_data}


def workDataVersion(data):
    try:
        final_data = {}
        for d in data:
            d = d.replace('\r\n', '')
            if 'Base ethernet MAC Address' in d:
                final_data['Base ethernet MAC Address'] = d.split(': ')[1]
            elif 'Motherboard assembly number' in d:
                final_data['Motherboard assembly number'] = d.split(': ')[1]
            elif 'Power supply part number' in d:
                final_data['Power supply part number'] = d.split(': ')[1]
            elif 'Motherboard serial number' in d:
                final_data['Motherboard serial number'] = d.split(': ')[1]
            elif 'Power supply serial number' in d:
                final_data['Power supply serial number'] = d.split(': ')[1]
            elif 'Model revision number' in d:
                final_data['Model revision number'] = d.split(': ')[1]
            elif 'Motherboard revision number' in d:
                final_data['Motherboard revision number'] = d.split(': ')[1]
            elif 'Model number' in d:
                final_data['Model number'] = d.split(': ')[1]
            elif 'System serial number' in d:
                final_data['System serial number'] = d.split(': ')[1]
    except Exception as e:
        return {'success': False, 'error': 'Error to work data!'}
    return {'success': True, 'data': [final_data]}


class SwitchConnector:
    def __init__(self, log, username, password, switch, command, args=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.log = log
        self.username = username
        self.password = password
        self.switch = switch
        self.command = command
        self.args = args

    def setCommand(self, command):
        self.command = command

    def setArgs(self, args):
        self.args = args

    def runGet(self):
        data = self.connectSwitchGet()
        if data['success']:
            data = initialData(data['data'])
            if data['success']:
                if self.command == 'show version':
                    data = workDataVersion(data['data'])
                else:
                    data = workData(data['data'])
        self.log.debug(data)
        return data

    def runPost(self):
        data = self.connectSwitchPost()
        self.log.debug(data)
        return data

    def connectSwitchGet(self):
        try:
            self.ssh.connect(self.switch, username=self.username, password=self.password, look_for_keys=False,
                             timeout=None)
            try:
                ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(self.command)
                data = ssh_stdout.readlines()
            except Exception as e:
                return {'success': False, 'error': 'Error to execute commands!'}
            self.ssh.close()
        except Exception as e:
            return {'success': False, 'error': 'Error to connect!'}
        return {'success': True, 'data': data}

    def connectSwitchPost(self):
        cmd_to_execute = self.editCommands()
        try:
            self.ssh.connect(self.switch, username=self.username, password=self.password, look_for_keys=False,
                             timeout=None)
            try:
                connection = self.ssh.invoke_shell()
                for c in cmd_to_execute:
                    time.sleep(1)
                    connection.send(c + '\n')
                time.sleep(1)
            except Exception as e:
                return {'success': False, 'error': 'Error to execute commands!'}
            self.ssh.close()
        except Exception as e:
            return False, 'Error to connect!'
        return{'success': True, 'text': 'Success!'}

    def editCommands(self):
        exec_c = None
        if self.command == 'change_vlan':
            exec_c = POST_COMMANDS['change_vlan']
            exec_c[1] = exec_c[1].format(self.args['inter'])
            exec_c[3] = exec_c[3].format(self.args['vlan'])
        elif self.command == 'create_vlan':
            exec_c = POST_COMMANDS['create_vlan']
            exec_c[1] = exec_c[1].format(self.args['vlan'])
            if 'name' in self.args:
                exec_c[2] = exec_c[2].format(self.args['name'])
            else:
                del exec_c[2]
        elif self.command == 'delete_vlan':
            exec_c = POST_COMMANDS['delete_vlan']
            exec_c[1] = exec_c[1].format(self.args['vlan'])
        return exec_c
