from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from .loginform import UserLoginForm
from .registerform import UserRegisterForm
from .searchform import StreetRiskForm
from .routeform import StreetRouteForm
from .reportform import StreetReportForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import requests, asyncio, httpx
from asgiref.sync import async_to_sync, sync_to_async

async def make_async_api_call(url: str, headers: dict) -> dict:
    async with httpx.AsyncClient(timeout=httpx.Timeout(25.0, connect=1.0)) as client:
        response = await client.get(url, headers=headers)

    return response.json()['results']

def index(request):
    context = {
        'loggedin': False
    }

    if 'Authorization' in request.session.keys():
        headers = {'Authorization': request.session['Authorization']}
        api_user_url = 'http://'+str(get_current_site(request))+'/api/auth/users/' 
        response = requests.get(api_user_url, headers=headers)
        
        if not response.status_code == 401:
            context['loggedin'] = True

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
    context = {
        'loggedin': True
    }

    if request.method == 'POST':
        form = StreetRiskForm(request.POST, initial={'street': 'Via'})

        if form.is_valid():
            headers = {
                'Authorization': request.session.get('Authorization')
            }

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

            base_url = 'http://'+str(get_current_site(request))
            response = (requests.get(base_url+'/api/getriskdata?street='+street+''+time_url, headers=headers)).json()['results']
            
            street_data = response['risk_metadata']
            for data in street_data:
                data['reference'] = {}
                data['reference'][data['news']] = data['link']
                data.pop('id')
                data.pop('news')
                data.pop('link')
                data.pop('street')
            
            context['street'] = street
            context['street_data'] = street_data
            context['timeline_data'] = response['all_timeline']
            context['tag_data'] = response['all_tags']
            context['user_reported_timeline_data'] = response['user_timeline']
            context['user_reported_tag_data'] = response['user_tags']
            context['risk_score'] = response['risk_score']
            context['top_time'] = response['all_top_timeline']
            context['top_tags'] = response['all_top_tag']

    else:
        form = StreetRiskForm(initial={'street': 'Via'})

    context['form'] = form
    
    return render(request,'streets.html', context)

@sync_to_async
@login_required
@async_to_sync
async def route(request):
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

                risk_data = await asyncio.gather(*[make_async_api_call('http://'+str(get_current_site(request))+'/api/getriskdata?street='+street, headers) for street in all_streets])
                for street in response['results']:
                    for data in risk_data:
                        if street['name'] == data['street']:
                            street['risk_data'] = data

                    if street['risk_data']['risk_score'] == 'Moderately Unsafe' and street['name'] not in moderate_streets: moderate_streets.append(street['name'])
                    if street['risk_data']['risk_score'] == 'Unsafe' and street['name'] not in unsafe_streets: unsafe_streets.append(street['name'])
                
                    tag_data = street['risk_data']['all_tags']
                    if len(tag_data.keys()) > 0:
                        street['tag_data'] = ', '.join(tag_data.keys())
                        
                    context['route_data'] = response['results'],
                    context['moderate_streets'] = moderate_streets,
                    context['unsafe_streets'] = unsafe_streets,
                    context['all_streets'] = ' -> '.join(all_streets)
            else:
                context['message'] = response['errors'][0]

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