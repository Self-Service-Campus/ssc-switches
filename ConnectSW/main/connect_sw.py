import paramiko

switches = ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt']
commands = ['show arp', 'show interfaces status', 'show version']

username = 'root'
password = 'DETi4sw'
server = username + '@' + switches[0]


def conSW(switch, cmd_to_execute):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(switch, username=username, password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

    data = ssh_stdout.readlines()[15:]
    # worked_data = ['<pre class="tab">'+x+'spaces</pre>' for x in data]
    # print(worked_data)
    return data
