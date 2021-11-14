from django.shortcuts import render, redirect
from django.db.models import Count
from .searchform import StreetRiskForm

from ProMeAPI.models import StreetRisk

def streets(request):
    risk_score = StreetRisk.objects.all().order_by('street_name').values('street_name').annotate(count=Count('street_name'))

    if request.method == 'POST':
        form = StreetRiskForm(request.POST)

        if form.is_valid():
            form = StreetRisk.objects.filter(street_name=request.POST.get('street_name'))
            return redirect('/web/streetrisk?street='+request.POST.get('street_name'))
        else:
            print('Error')

    else:
        form = StreetRiskForm()

    context = {
        'risk_score': risk_score,
        'form': form,
    }
    return render(request,'streets.html', context)



def streetrisk(request):
    street_name = request.GET.get('street')
    data = StreetRisk.objects.filter(street_name=street_name).values('date').annotate(count=Count('street_name'))

    if request.method == 'POST':
        form = StreetRiskForm(request.POST)

        if form.is_valid():
            form = StreetRisk.objects.filter(street_name=request.POST.get('street_name'))
            return redirect('/web/streetrisk?street='+request.POST.get('street_name'))
        else:
            print('Error')

    else:
        form = StreetRiskForm()

    context = {
        'data': data,
        'form': form,
    }
    return render(request,'streetrisk.html', context)