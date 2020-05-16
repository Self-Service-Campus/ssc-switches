import paramiko
import re
import time

INSTRUCTIONS = {'create_vlan': ['config t', 'vlan {}', 'end'],
                 'delete_vlan': ['config t', 'no vlan {}', 'end'],
                 'change_vlan': ['config t', 'int {}', 'switchport mode access', 'switch access vlan {}', 'end']}


def removeInitialFrame(data):
    try:
        data = data[14:]
        while data[0] == '\r\n':
            data = data[1:]
        initial_data = data
    except Exception as e:
        return {'success': False, 'error': 'Error to work initial data!'}
    return {'success': True, 'data': initial_data}


def show(data):
    try:
        header = data[0]
        header = header.replace('\r\n', '')
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


def showVersion(data):
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


def showInterfaceSwitchPort(data):
    try:
        ports = []
        port = {}
        for d in data:
            d = d.replace('\r\n', '')
            if d == '':
                ports.append(port)
                port = {}
            else:
                x = d.split(': ')
                if len(x) == 2:
                    port[x[0]] = x[1]
    except Exception as e:
        return {'success': False, 'error': 'Error to get Ports!'}
    return {'success': True, 'data': ports}


def showPortSecurityInterface(data):
    try:
        ports = []
        port = {}
        for d in data:
            d = d.replace('\r\n', '')
            x = d.split(': ')
            if len(x) == 2:
                port[x[0]] = x[1]
    except Exception as e:
        return {'success': False, 'error': 'Error to get Ports!'}
    return {'success': True, 'data': ports}


def getCommands(instruction, args):
    commands = INSTRUCTIONS[instruction]
    if instruction == 'change_vlan':
        if 'interface' not in args or 'vlan' not in args:
            return {'success': False, 'error': 'Missing arguments!'}
        commands[1] = commands[1].format(args['interface'])
        commands[3] = commands[3].format(args['vlan'])
    elif instruction == 'create_vlan':
        if 'vlan' not in args:
            return {'success': False, 'error': 'Missing arguments!'}
        commands[1] = commands[1].format(args['vlan'])
        if 'name' in args:
            commands.insert(2, 'name ' + args['name'])
    elif instruction == 'delete_vlan':
        if 'vlan' not in args:
            return {'success': False, 'error': 'Missing arguments!'}
        commands[1] = commands[1].format(args['vlan'])
    return {'success': True, 'commands': commands}


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

    def run(self):
        if self.command in INSTRUCTIONS:
            data = getCommands(self.command, self.args)
            if data['success']:
                data = self.connectSwitchPost(data['commands'])
        else:
            data = self.connectSwitchGet()
            if data['success']:
                data = removeInitialFrame(data['data'])
                if data['success']:
                    if self.command == 'show version':
                        data = showVersion(data['data'])
                    elif self.command == 'show interface switchport':
                        data = showInterfaceSwitchPort(data['data'])
                    elif 'show port-security interface' in self.command:
                        data = showPortSecurityInterface(data['data'])
                    else:
                        data = show(data['data'])
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

    def connectSwitchPost(self, commands):
        try:
            self.ssh.connect(self.switch, username=self.username, password=self.password, look_for_keys=False,
                             timeout=None)
            try:
                connection = self.ssh.invoke_shell()
                for commmand in commands:
                    time.sleep(1)
                    connection.send(commmand + '\n')
                time.sleep(1)
            except Exception as e:
                return {'success': False, 'error': 'Error to execute commands!'}
            self.ssh.close()
        except Exception as e:
            return False, 'Error to connect!'
        return{'success': True, 'text': 'Success!'}
