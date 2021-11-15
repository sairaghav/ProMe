from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .searchform import StreetRiskForm


import requests, json, datetime

import collections

def get_tag_data(result, source='News'):
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

def get_timeline_data(result, source='News'):
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

def streets(request):
    if request.method == 'POST':
        form = StreetRiskForm(request.POST,
            initial={'street': 'Lambrate',
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

            print(user_reported_timeline_data, user_reported_tag_data)
            
            context = {
                'timeline_data': timeline_data,
                'tag_data': tag_data,
                'form': form,
                'street': street,
                'street_data': street_data,
                'user_reported_timeline_data': user_reported_timeline_data,
                'user_reported_tag_data': user_reported_tag_data,
            }
        else:
            print('Error')

    else:
        form = StreetRiskForm(initial={'street': 'Lambrate',
                        'news_from': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=30)).strftime("%Y-%m-%d"), 
                        'news_till': datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
                    }
                )
        context = {
            'form': form
        }

    

    return render(request,'streets.html', context)