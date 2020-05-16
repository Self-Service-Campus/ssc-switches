from __future__ import absolute_import
from celery import shared_task
from main.SwitchConnector import SwitchConnector
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


@shared_task
def runGet(username, password, switch_ip, command):
    connector = SwitchConnector(logger, username, password, switch_ip, command)
    return connector.run()


@shared_task
def runPost(username, password, switch_ip, command, args):
    connector = SwitchConnector(logger, username, password, switch_ip, command, args)
    return connector.run()


@shared_task
def loadDataToDB(username, password, switches_ip):
    load_data = []
    for switch_ip in switches_ip:
        connector = SwitchConnector(logger, username, password, switch_ip, 'show version')
        data = connector.run()
        if not data['success']:
            return data
        switch = {'id_switch': switch_ip.replace('.ua.pt', ''), 'ip_switch': switch_ip,
                  'model_switch': data['data'][0]['Model number']}
        connector.setCommand('show interfaces status')
        data = connector.run()
        if not data['success']:
            return data
        data = getPorts(switch_ip, data['data'])
        if not data['success']:
            return data
        ports = {'switch': switch, 'ports': data['data']}
        load_data.append(ports)
    return {'success': True, 'data': load_data}


@shared_task
def consultPortStatus(username, password, switch_ip):
    connector = SwitchConnector(logger, username, password, switch_ip, 'show interface switchport')
    return connector.run()

