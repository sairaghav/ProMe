from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

from .loginform import UserLoginForm
from .registerform import UserRegisterForm
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

def index(request):
    if 'Authorization' in request.session.keys():
        return redirect('/streets')
    else:

        return redirect('/login')

def register(request):
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
                messages.error(request, response.text)
        else:
            messages.error(request, 'Enter all details')


    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'loggedin': False
    }


    return render(request,'register.html', context)
    
def signin(request):
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
            token = json.loads(response.text)['auth_token']
            request.session['Authorization'] = 'Token '+token
            
            return redirect('/streets')
        else:
            messages.error(request, 'Email or password is incorrect')

    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'loggedin': False
    }


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

            headers = {
                'Authorization': request.session.get('Authorization')
            }
            response = requests.get('http://'+str(get_current_site(request))+'/api/news?street='+street+'&from='+from_date+'&to='+to_date, headers=headers)
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
            'form': form,
            'loggedin': True
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

            post_data = {
                'street': street,
                'tags': tags,
                'summary': summary
            }

            headers = {
                'Authorization': request.session.get('Authorization')
            }

            response = requests.post('http://'+str(get_current_site(request))+'/api/report', data=post_data, headers=headers)

            messages.success(request, 'Incident reported successfully')

        else:
            message = 'There is some error in your report. Please check again.'

        context = {
            'message': message,
            'form': form,
            'loggedin': True
        }

    else:
        form = StreetReportForm()
        context = {
            'form': form,
            'loggedin': True
        }

    return render(request, 'report.html', context)