import json

from django.shortcuts import render


def main(request):
    h = json.load(open('result.json'))
    l = [holder['account'] for holder in h]
    d = [holder['balance'] for holder in h]
    return render(request, 'chartApp/index.html', {'labels': l, 'data': d})
