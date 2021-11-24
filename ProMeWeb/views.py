from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

from .loginform import UserLoginForm
from .registerform import UserRegisterForm
from .searchform import StreetRiskForm
from .routeform import StreetRouteForm
from .reportform import StreetReportForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import requests, datetime

def index(request):
    return render(request,'index.html')

def register(request):
    context = {
        'loggedin': False
    }

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')

            post_data = {
                'username': user,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone
            }

            api_register_url = 'http://'+str(get_current_site(request))+'/api/auth/users/'
            response = requests.post(api_register_url, data=post_data)

            if response.status_code == 201:
                return redirect('/login')
            else:
                context['message'] = response.text

    else:
        form = UserRegisterForm()

    context['form'] = form

    return render(request,'register.html', context)
    
def signin(request):
    context = {
        'loggedin': False
    }

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        email = request.POST.get('email')
        password = request.POST.get('password')

        post_data = {
            'email': email,
            'password': password
        }

        auth = authenticate(request, username=email, password=password)
        
        if auth is not None:
            login(request, auth)

            api_login_url = 'http://'+str(get_current_site(request))+'/api/auth/token/login'
            response = requests.post(api_login_url, data=post_data)
            token = response.json()['auth_token']
            request.session['Authorization'] = 'Token '+token
            
            return redirect('/streets')
        else:
            context['message'] = 'Email or password is incorrect'

    else:
        form = UserLoginForm()

    context['form'] = form

    return render(request,'login.html', context)

@login_required
def logout(request):
    if request.method == 'GET':
        headers = {
            'Authorization': request.session.get('Authorization')
        }
        api_logout_url = 'http://'+str(get_current_site(request))+'/api/auth/token/logout'
        response = requests.post(api_logout_url, headers=headers)
        request.session.flush()
    
    return redirect('/login')

@login_required
def streets(request):
    street = request.POST.get('street', None)
    from_date = None if request.POST.get('news_from') == '' else request.POST.get('news_from')
    to_date = None if request.POST.get('news_till') == '' else request.POST.get('news_till')

    context = {
        'loggedin': True
    }

    if request.method == 'POST' and street is not None:
        form = StreetRiskForm(request.POST, initial={'street': 'Via'})

        if form.is_valid():
            headers = {
                'Authorization': request.session.get('Authorization')
            }
            if from_date is None or to_date is None:
                response = requests.get('http://'+str(get_current_site(request))+'/api/news?street='+street, headers=headers)
                time_range = 14
            else:
                response = requests.get('http://'+str(get_current_site(request))+'/api/news?street='+street+'&from='+from_date+'&to='+to_date, headers=headers)
                time_range = (datetime.datetime.strptime(to_date,'%Y-%m-%d') - datetime.datetime.strptime(from_date,'%Y-%m-%d')).days
            
            street_data = response.json()['results']

            for data in street_data:
                data['reference'] = {}
                data['reference'][data['news']] = data['link']
                data.pop('id')
                data.pop('news')
                data.pop('link')

            timeline_data = (requests.get('http://'+str(get_current_site(request))+'/api/gettimeline?street='+street, headers=headers)).json()['results']
            tag_data = (requests.get('http://'+str(get_current_site(request))+'/api/gettags?street='+street, headers=headers)).json()['results']
            user_reported_timeline_data = (requests.get('http://'+str(get_current_site(request))+'/api/gettimeline?street='+street+'&source=User', headers=headers)).json()['results']
            user_reported_tag_data = (requests.get('http://'+str(get_current_site(request))+'/api/gettags?street='+street+'&source=User', headers=headers)).json()['results']
            
            risk_value = len(street_data)/time_range
            if risk_value <= 0.1:
                risk_score = 'Safe'
            elif risk_value <= 0.25:
                risk_score = 'Moderately Safe'
            else:
                risk_score = 'Unsafe'
            
            context['timeline_data'] = timeline_data
            context['tag_data'] = tag_data
            context['street'] = street
            context['street_data'] = street_data
            context['user_reported_timeline_data'] = user_reported_timeline_data
            context['user_reported_tag_data'] = user_reported_tag_data
            context['risk_score'] = risk_score

    else:
        form = StreetRiskForm(initial={'street': 'Via'})

    context['form'] = form
    
    return render(request,'streets.html', context)

@login_required
def route(request):
    context = {
        'loggedin': True
    }

    if request.method == 'POST':
        form = StreetRouteForm(request.POST, initial={
            'source': 'Via',
            'destination': 'Via',
            'mode': 'pedestrian'
        })

        if form.is_valid():
            headers = {
                'Authorization': request.session.get('Authorization')
            }

            start = request.POST.get('source')
            end = request.POST.get('destination') 
            mode = request.POST.get('mode')

            response = (requests.get('http://'+str(get_current_site(request))+'/api/directions?start='+start+'&end='+end+'&mode='+mode, headers=headers)).json()
            
            all_streets= []
            moderate_streets = []
            unsafe_streets = []
            
            if response['results'] is not None:
                for street in response['results']:
                    if street['name'] not in all_streets: all_streets.append(street['name'])
            
                    if street['risk_score'] <= 0.1: street['risk_value'] = 'Safe'
                    elif street['risk_score'] <= 0.25: street['risk_value'] = 'Moderately Safe'
                    else: street['risk_value'] = 'Unsafe'
                    
                    if street['risk_value'] == 'Moderately Safe' and street['name'] not in moderate_streets: moderate_streets.append(street['name'])
                    if street['risk_value'] == 'Unsafe' and street['name'] not in unsafe_streets: unsafe_streets.append(street['name'])

                    
                context['route_data'] = response['results'],
                context['moderate_streets'] = moderate_streets,
                context['unsafe_streets'] = unsafe_streets,
                context['all_streets'] = ' -> '.join(all_streets)
        
            else:
                context['message'] = response['errors']

    else:
        form = StreetRouteForm(initial={
            'source': 'Via',
            'destination': 'Via',
            'mode': 'pedestrian'
        })

    context['form'] = form

    return render(request,'route.html', context)
    
@login_required
def report(request):
    context = {
        'loggedin': True
    }

    if request.method == 'POST':
        form = StreetReportForm(request.POST)
        message = ''

        if form.is_valid():
            street = request.POST.get('street')
            tags = request.POST.get('tags')
            summary = request.POST.get('news')

            headers = {
                'Authorization': request.session.get('Authorization')
            }

            response = requests.get('http://'+str(get_current_site(request))+'/api/auth/users/me', headers=headers)
            user = response.json()['username']


            post_data = {
                'street': street,
                'tags': tags,
                'summary': summary,
                'user': user
            }

            requests.post('http://'+str(get_current_site(request))+'/api/report', data=post_data, headers=headers)

            context['message'] = 'Incident reported successfully'

        else:
            context['message'] = 'There is some error in your report. Please check again.'


    else:
        form = StreetReportForm()
    
    context['form'] = form

    return render(request, 'report.html', context)