from __future__ import absolute_import
from celery import shared_task
from main.SwitchConnector import SwitchConnector, getPorts
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task
def runGet(username, password, switch_ip, command):
    connector = SwitchConnector(logger, username, password, switch_ip, command)
    return connector.runGet()


@shared_task
def runPost(username, password, switch_ip, command, args):
    connector = SwitchConnector(logger, username, password, switch_ip, command, args)
    return connector.runPost


@shared_task
def loadDataToDB(username, password, switches_ip):
    load_data = []
    for switch_ip in switches_ip:
        connector = SwitchConnector(logger, username, password, switch_ip, 'show version')
        data = connector.runGet()
        if not data['success']:
            return data
        switch = {'id_switch': switch_ip.replace('.ua.pt', ''), 'ip_switch': switch_ip,
                  'model_switch': data['data']['Model number']}
        connector.setCommand('show interfaces status')
        data = connector.runGet()
        if not data['success']:
            return data
        data = getPorts(switch_ip, data['data'])
        if not data['success']:
            return data
        ports = {'switch': switch, 'ports': data['data']}
        load_data.append(ports)

    # ------------------------------------- #
    # Falta fazer load para a base de dados #
    # ------------------------------------- #

    return {'success': True, 'data': load_data}
