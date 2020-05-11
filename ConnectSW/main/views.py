from django.shortcuts import render
from main.tasks import runGet


# Create your views here.
def homepage(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        command = request.POST.get('command')
        sinc = request.POST.get('sinc')
        return show(request, switch, command, sinc)
    params = {
        'switches': ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt'],
        'commands': ['show arp', 'show interfaces status', 'show version']
    }
    return render(request, 'index.html', params)


def show(request, switch, command, sinc):
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
    return render(request, 'show.html', params)
