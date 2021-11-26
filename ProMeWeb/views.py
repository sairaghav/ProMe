from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from .loginform import UserLoginForm
from .registerform import UserRegisterForm
from .searchform import StreetRiskForm
from .routeform import StreetRouteForm
from .reportform import StreetReportForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import requests

def index(request):
    context = {
        'loggedin': False
    }
    if 'Authorization' in request.session.keys():
        context = {
        'loggedin': True
    }

    return render(request,'index.html', context)

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

            base_url = 'http://'+str(get_current_site(request))
            api_register_url = base_url+'/api/auth/users/'
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

            base_url = 'http://'+str(get_current_site(request))
            api_login_url = base_url+'/api/auth/token/login'
            response = requests.post(api_login_url, data=post_data)
            token = response.json()['auth_token']
            request.session['Authorization'] = 'Token '+token
            
            return redirect('/')
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

        base_url = 'http://'+str(get_current_site(request))
        api_logout_url = base_url+'/api/auth/token/logout'
        requests.post(api_logout_url, headers=headers)
        request.session.flush()
    
    return redirect('/login')

@login_required
def streets(request):
    street = request.POST.get('street', None)
    from_date = None if request.POST.get('news_from') == '' else request.POST.get('news_from')
    to_date = None if request.POST.get('news_till') == '' else request.POST.get('news_till')

    if from_date is None and to_date is None:
        time_url = ''
    elif from_date is None:
        time_url = '&to='+to_date
    elif to_date is None:
        time_url = '&from='+from_date
    else:
        time_url = '&from='+from_date+'&to='+to_date

    context = {
        'loggedin': True
    }

    if request.method == 'POST' and street is not None:
        form = StreetRiskForm(request.POST, initial={'street': 'Via'})

        if form.is_valid():
            headers = {
                'Authorization': request.session.get('Authorization')
            }

            base_url = 'http://'+str(get_current_site(request))

            response = requests.get(base_url+'/api/news?street='+street+''+time_url, headers=headers)
            timeline_data = (requests.get(base_url+'/api/getmetadata?street='+street+''+time_url+'&type=timeline', headers=headers)).json()['results']
            tag_data = (requests.get(base_url+'/api/getmetadata?street='+street+''+time_url+'&type=tags', headers=headers)).json()['results']
            risk_score = (requests.get(base_url+'/api/getriskscore?street='+street+''+time_url, headers=headers)).json()['results']
            top_time = (requests.get(base_url+'/api/getmetadata?street='+street+''+time_url+'&type=timeline&limit=3', headers=headers)).json()['results']['all']
            top_tags = (requests.get(base_url+'/api/getmetadata?street='+street+''+time_url+'&type=tags&limit=3', headers=headers)).json()['results']['all']
            
            street_data = response.json()['results']
            all_timeline_data = timeline_data['all']
            all_tag_data = tag_data['all']
            user_reported_timeline_data = timeline_data['user']
            user_reported_tag_data = tag_data['user']

            for data in street_data:
                data['reference'] = {}
                data['reference'][data['news']] = data['link']
                data.pop('id')
                data.pop('news')
                data.pop('link')
                data.pop('street')
            
            context['timeline_data'] = all_timeline_data
            context['tag_data'] = all_tag_data
            context['street'] = street
            context['street_data'] = street_data
            context['user_reported_timeline_data'] = user_reported_timeline_data
            context['user_reported_tag_data'] = user_reported_tag_data
            context['risk_score'] = risk_score
            context['top_time'] = top_time
            context['top_tags'] = top_tags

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

            base_url = 'http://'+str(get_current_site(request))
            response = (requests.get(base_url+'/api/directions?start='+start+'&end='+end+'&mode='+mode, headers=headers)).json()
            
            all_streets= []
            moderate_streets = []
            unsafe_streets = []
            
            if response['results'] is not None:
                for street in response['results']:
                    if street['name'] not in all_streets: all_streets.append(street['name'])
                    if street['risk_score'] == 'Moderately Safe' and street['name'] not in moderate_streets: moderate_streets.append(street['name'])
                    if street['risk_score'] == 'Unsafe' and street['name'] not in unsafe_streets: unsafe_streets.append(street['name'])

                    
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

            base_url = 'http://'+str(get_current_site(request))
            response = requests.get(base_url+'/api/auth/users/me', headers=headers)
            user = response.json()['username']


            post_data = {
                'street': street,
                'tags': tags,
                'summary': summary,
                'user': user
            }

            requests.post(base_url+'/api/report', data=post_data, headers=headers)

            context['message'] = 'Incident reported successfully'

        else:
            context['message'] = 'There is some error in your report. Please check again.'


    else:
        form = StreetReportForm()
    
    context['form'] = form

    return render(request, 'report.html', context)