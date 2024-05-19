import requests
from django.shortcuts import render
import environ
from datetime import datetime, timedelta

# Create your views here.

env = environ.Env()

def fetch_entities(api_key, start_date, end_date, page_size=1000, filters=[]):
    # url = 'https://api.sam.gov/entity-information/v1/entities'
    url = "https://api.sam.gov/opportunities/v2/search"
    params = {
        'api_key': api_key,
        'postedFrpm': start_date,
        'postedTo': end_date,
        'limit': page_size,
    }

    for filter_param in filters:
        params.update(filter_param)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "entityData" in data:
            entities = data["entityData"]
            total_records = data["totalRecords"]
            print(f"Fetched {len(entities)} entities.")
            # print(f"Fetched {len(entities)} entities out of {total_records}")
            return entities, total_records
        else:
            print("No data found in the API response.")
            return [], 0
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return [], 0

def entity_list(request):
    api_key = env('API_KEY')
    last_how_many_days = 30
    start_date = (datetime.now() - timedelta(days=last_how_many_days)).strftime('%m-%d-%Y')
    end_date = datetime.now().strftime('%m-%d-%Y')
    entities, total_records = fetch_entities(api_key, start_date, end_date)
    # return render(request, 'sam_api/entity_list.html', {'entities': entities, 'total_records': total_records})
    return render(request, 'sam_api/entity_list.html', {'entities': entities})

# def entity_list(request):
#     api_key = env('API_KEY')
#     api_url = 'https://api.sam.gov/entity-information/v1/entities'
#     params = {'api_key': api_key}

#     try:
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         entities = data.get('entityData', [])
#     except requests.RequestException as e:
#         print("Request error:", e)
#         entities = []
    
#     print(api_key)

#     return render(request, 'sam_api/entity_list.html', {'entities': entities})