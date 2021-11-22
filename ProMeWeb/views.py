from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from .loginform import UserLoginForm
from .searchform import StreetRiskForm
from .reportform import StreetReportForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



import requests, json, datetime

import collections

def get_tag_data(result, source='All'):
    data = []

    for value in result:
        to_consider = True
        if source == 'User' and not value['source'].startswith('User'):
            to_consider = False
        else:
            to_consider = True
        if to_consider:
            for tag in value['tags'].split(','):
                data.append(tag)

    counter = collections.Counter(data)

    if len(dict(counter).keys()) > 0:
        return dict(counter)

    else:
        return None

def get_timeline_data(result, source='All'):
    data = []

    for value in result:
        to_consider = True
        if source == 'User' and not value['source'].startswith('User'):
            to_consider = False
        if to_consider:
            date = datetime.datetime.strptime(value['date'].split('T')[0],"%Y-%m-%d").strftime('%B %Y')
            data.append(date)

    counter = collections.Counter(data)
    
    if len(dict(counter).keys()) > 0:
        return dict(counter)

    else:
        return None

def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            user = request.POST.get('username')
            password = request.POST.get('password')

            data = {
                'email': user,
                'password': password
            }
            auth = authenticate(request, username=user, password=password)

            if auth is not None:
                login(request, auth)
                return redirect('/streets')
            else:
                messages.error(request, 'Username or password is incorrect')


    else:
        form = UserLoginForm()

    context = {
        'form': form
    }


    return render(request,'login.html', context)

@login_required
def streets(request):
    if request.method == 'POST':
        form = StreetRiskForm(request.POST,
            initial={'street': 'Via',
                        'news_from': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=30)).strftime("%Y-%m-%d"), 
                        'news_till': datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
                    }
        )

        if form.is_valid():
            street = request.POST.get('street')
            from_date = request.POST.get('news_from') 
            to_date = request.POST.get('news_till') 
            
            response = requests.get('http://'+str(get_current_site(request))+'/api/news?street='+street+'&from='+from_date+'&to='+to_date)
            street_data = json.loads(response.text)['results']

            for data in street_data:
                data['reference'] = {}
                data['reference'][data['news']] = data['link']
                data.pop('id')
                data.pop('news')
                data.pop('link')
            timeline_data = get_timeline_data(street_data)
            tag_data = get_tag_data(street_data)
            user_reported_timeline_data = get_timeline_data(street_data, 'User')
            user_reported_tag_data = get_tag_data(street_data, 'User')

            time_range = (datetime.datetime.strptime(to_date,"%Y-%m-%d")-datetime.datetime.strptime(from_date,"%Y-%m-%d")).days
            risk_value = len(street_data)/time_range if time_range > 0 else len(street_data)
            if risk_value <= 0.1:
                risk_score = 'Safe'
            elif risk_value <= 0.25:
                risk_score = 'Moderately Safe'
            else:
                risk_score = 'Unsafe'
            
            context = {
                'timeline_data': timeline_data,
                'tag_data': tag_data,
                'form': form,
                'street': street,
                'street_data': street_data,
                'user_reported_timeline_data': user_reported_timeline_data,
                'user_reported_tag_data': user_reported_tag_data,
                'risk_score': risk_score
            }
        else:
            print('Error')

    else:
        form = StreetRiskForm(initial={'street': 'Via',
                        'news_from': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=30)).strftime("%Y-%m-%d"), 
                        'news_till': datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
                    }
                )
        context = {
            'form': form
        }

    

    return render(request,'streets.html', context)

@login_required
def report(request):
    if request.method == 'POST':
        form = StreetReportForm(request.POST)
        message = ''

        if form.is_valid():
            street = request.POST.get('street')
            tags = request.POST.get('tags')
            summary = request.POST.get('news')

            response = requests.get('http://'+str(get_current_site(request))+'/api/report?street='+street+'&tags='+tags+'&summary='+summary)
            messages.success(request, 'Incident reported successfully')

        else:
            message = 'There is some error in your report. Please check again.'

        context = {
            'message': message,
            'form': form
        }

    else:
        form = StreetReportForm()
        context = {
            'form': form
        }

    return render(request, 'report.html', context)