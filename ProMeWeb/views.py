from django.shortcuts import render, redirect
from django.db.models import Count
from .searchform import StreetRiskForm

from ProMeAPI.models import StreetRisk

import collections

def get_tag_data(result):
    data = []

    for value in result:
        value = list(value)
        for tag in value[0].split(','):
            data.append(tag)

    counter = collections.Counter(data)

    if len(dict(counter).keys()) > 0:
        return dict(counter)

    else:
        return None

def get_timeline_data(result):
    data = []
    for value in result:
        value = list(value)
        value[0] = (value[0].strftime("%B %Y"))
        data.append(value[0])

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
            return redirect('/streets?street='+request.POST.get('street_name'))
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
    street_name = request.GET.get('street')
    timeline_data = get_timeline_data(StreetRisk.objects.filter(street_name=street_name).values_list('date'))
    tag_data = get_tag_data(StreetRisk.objects.filter(street_name=street_name).values_list('tags'))

    if request.method == 'POST':
        form = StreetRiskForm(request.POST)

        if form.is_valid():
            form = StreetRisk.objects.filter(street_name=request.POST.get('street_name'))
            return redirect('/streets?street='+request.POST.get('street_name'))
        else:
            print('Error')

    else:
        form = StreetRiskForm()

    context = {
        'timeline_data': timeline_data,
        'tag_data': tag_data,
        'form': form,
        'street': street_name,
    }

    return render(request,'streets.html', context)