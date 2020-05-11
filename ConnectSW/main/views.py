from django.shortcuts import render
from main.tasks import runGet, runPost, loadDataToDB


# Create your views here.
def homepage(request):
    return render(request, 'index.html')


def show(request, params):
    return render(request, 'show.html', params)


def runget(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        command = request.POST.get('command')
        sinc = request.POST.get('sinc')
        params = {
            'data': ['data']
        }
        if sinc == 'sinc':
            data = runGet('root', 'DETi4sw', switch, command)
            if data['success']:
                params['data'] = data['data']
            else:
                params['data'] = data['text']
        else:
            runGet.delay('root', 'DETi4sw', switch, command)
        return show(request, params)
    params = {
        'switches': ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt'],
        'commands': ['show arp', 'show interfaces status', 'show version']
    }
    return render(request, 'runget.html', params)


def runpost(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        command = request.POST.get('command')
        args = {'inter': request.POST.get('inter'), 'name': request.POST.get('name'), 'vlan': request.POST.get('vlan')}
        runPost.delay('root', 'DETi4sw', switch, command, args)
        return show(request, {'data': ['data']})
    params = {
        'switches': ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt'],
        'commands': ['create_vlan', 'delete_vlan', 'change_vlan']
    }
    return render(request, 'runpost.html', params)


def loaddata(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        command = request.POST.get('command')
        sinc = request.POST.get('sinc')
        params = {
            'data': ['data']
        }
        if sinc == 'sinc':
            data = loadDataToDB('root', 'DETi4sw', [switch])
            if data['success']:
                params['data'] = data['data']
            else:
                params['data'] = data['text']
        else:
            loadDataToDB.delay('root', 'DETi4sw', [switch])
        return show(request, params)
    params = {
        'switches': ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt']
    }
    return render(request, 'loaddata.html', params)
