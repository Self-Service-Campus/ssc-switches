from django.shortcuts import render
from main.connect_sw import conSW


# Create your views here.
def homepage(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        command = request.POST.get('command')
        return show(request, switch, command)
    params = {
        'switches': ['detiLab-b01-sw01.ua.pt', 'detiLab-b01-sw02.ua.pt', 'detiLab-b02-sw01.ua.pt'],
        'commands': ['show arp', 'show interfaces status', 'show version']
    }
    return render(request, 'index.html', params)


def show(request, switch, command):
    params = {
        'data': conSW(switch, command)
    }
    return render(request, 'show.html', params)