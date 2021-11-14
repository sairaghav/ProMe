from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .searchform import StreetRiskForm

from ProMeAPI.models import StreetRisk
import requests, json, datetime

import collections

def get_tag_data(result):
    data = []

    for value in result:
        for tag in value['tags'].split(','):
            data.append(tag)

    counter = collections.Counter(data)

    if len(dict(counter).keys()) > 0:
        return dict(counter)

    else:
        return None

def get_timeline_data(result):
    data = []
    for value in result:
        value['date'] = datetime.datetime.strptime(value['date'].split('T')[0],"%Y-%m-%d").strftime('%B %Y')
        data.append(value['date'])

    counter = collections.Counter(data)
    
    if len(dict(counter).keys()) > 0:
        return dict(counter)

    else:
        return None


def index(request):
    #risk_score = StreetRisk.objects.all().order_by('street_name').values('street_name').annotate(count=Count('street_name'))

    if request.method == 'POST':
        form = StreetRiskForm(request.POST)

        if form.is_valid():
            form = StreetRisk.objects.filter(street_name=request.POST.get('street_name'))
            return redirect('/streets')
        else:
            print('Error')

    else:
        form = StreetRiskForm()

    context = {
        #'risk_score': risk_score,
        'form': form,
    }
    return render(request,'streets.html', context)

def streets(request):
    if request.method == 'POST':
        form = StreetRiskForm(request.POST)

        if form.is_valid():
            street_name = request.POST.get('street_name')
            
            response = requests.get('http://'+str(get_current_site(request))+'/api/news?street='+street_name)
            
            street_data = json.loads(response.text)['results']
            timeline_data = get_timeline_data(street_data)
            tag_data = get_tag_data(street_data)
            
            context = {
                'timeline_data': timeline_data,
                'tag_data': tag_data,
                'form': form,
                'street': street_name,
                'street_data': street_data,
            }
        else:
            print('Error')

    else:
        form = StreetRiskForm()
        context = {
            'form': form
        }

    

    return render(request,'streets.html', context)