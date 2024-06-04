from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime, timedelta
# from .models import Opportunity
from .models_mongoengine import Opportunity
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import requests
import environ
import os
from pathlib import Path
# import time

# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ====================================================================================================

# def fetch_opportunities(api_key, start_date, end_date, page_size=1000, page=1, filters=[]):
#     url = "https://api.sam.gov/opportunities/v2/search"
#     params = {
#         'api_key': api_key,
#         'postedFrom': start_date,
#         'postedTo': end_date,
#         'limit': page_size,
#         'offset': (page - 1) * page_size,
#     }

#     for filter_param in filters:
#         params.update(filter_param)
    
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         print(f"Response data: {data}")
#         if "opportunitiesData" in data:
#             opportunities = data["opportunitiesData"]
#             total_records = data["totalRecords"]
#             print(f"Fetched {len(opportunities)} opportunities (Page {page}).")
#             return opportunities, total_records
#         else:
#             print("No data found in the API response.")
#             return [], 0
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred while making the request: {e}")
#         print(f"Response content: {response.content}")
#         if response.status_code == 429:
#             print("API rate limit exceeded. Waiting for 60 seconds.")
#             return None, 0
#         return [], 0

# def fetch_all_opportunities(api_key, start_date, end_date, page_size=1000, filters=[]):
#     all_opportunities = []
#     page = 1
#     total_records = 0
#     while True:
#         opportunities, records_count = fetch_opportunities(api_key, start_date, end_date, page_size, page, filters)
#         if opportunities is None:
#             time.sleep(60)
#             continue
#         all_opportunities.extend(opportunities)
#         total_records = records_count
#         if len(opportunities) < page_size:
#             break
#         page += 1
#     return all_opportunities, total_records

# def save_opportunities_to_db(opportunities):
#     for opp in opportunities:
#         award = opp.get("award", {})
#         awardee = award.get("awardee", {})
#         location = awardee.get("location", {})
#         place_of_performance = opp.get("placeOfPerformance", {})
#         place_of_performance_city = place_of_performance.get("city", {})
#         place_of_performance_country = place_of_performance.get("country", {})

#         Opportunity.objects.update_or_create(
#             notice_id=opp['noticeId'],
#             defaults={
#                 "title": opp.get("title"),
#                 "solicitation_number": opp.get("solicitationNumber"),
#                 "department": opp.get("department"),
#                 "sub_tier": opp.get("subTier"),
#                 "office": opp.get("office"),
#                 "posted_date": opp.get("postedDate"),
#                 "opportunity_type": opp.get("type"),
#                 "base_type": opp.get("baseType"),
#                 "archive_type": opp.get("archiveType"),
#                 "archive_date": opp.get("archiveDate"),
#                 "naics_code": opp.get("naicsCode"),
#                 "classification_code": opp.get("classificationCode"),
#                 "active": opp.get("active"),
#                 "award_date": award.get("date"),
#                 "award_number": award.get("number"),
#                 "award_amount": award.get("amount"),
#                 "awardee_name": awardee.get("name"),
#                 "awardee_street_address": location.get("streetAddress"),
#                 "awardee_city": location.get("city", {}).get("name"),
#                 "awardee_state": location.get("state", {}).get("code"),
#                 "awardee_zip": location.get("zip"),
#                 "awardee_country": location.get("country", {}).get("code"),
#                 "awardee_ueiSAM": awardee.get("ueiSAM"),
#                 "point_of_contact_email": opp.get("pointOfContact", [{}])[0].get("email"),
#                 "point_of_contact_phone": opp.get("pointOfContact", [{}])[0].get("phone"),
#                 "point_of_contact_name": opp.get("pointOfContact", [{}])[0].get("fullName"),
#                 "description": opp.get("description"),
#                 "organization_type": opp.get("organizationType"),
#                 "office_zipcode": opp.get("officeAddress", {}).get("zipcode"),
#                 "office_city": opp.get("officeAddress", {}).get("city"),
#                 "office_state": opp.get("officeAddress", {}).get("state"),
#                 "office_country_code": opp.get("officeAddress", {}).get("countryCode"),
#                 "place_of_performance_street_address": place_of_performance.get("streetAddress"),
#                 "place_of_performance_city": place_of_performance_city.get("name"),
#                 "place_of_performance_state": place_of_performance.get("state", {}).get("code"),
#                 "place_of_performance_zip": place_of_performance.get("zip"),
#                 "place_of_performance_country": place_of_performance_country.get("code"),
#                 "ui_link": opp.get("uiLink"),
#                 "additional_info_link": opp.get("additionalInfoLink"),
#             },
#         )

# def entity_list(request):
#     api_key = env('API_KEY')
#     last_how_many_days = 30
#     start_date = (datetime.now() - timedelta(days=last_how_many_days)).strftime('%m/%d/%Y')
#     end_date = datetime.now().strftime('%m/%d/%Y')

#     filters = [] # Define any filters if needed

#     all_opportunities, total_records = fetch_all_opportunities(api_key, start_date, end_date, page_size=1000, filters=filters)
#     save_opportunities_to_db(all_opportunities)
#     print(f"Total opportunities fetched and saved: {len(all_opportunities)} out of {total_records} records.")

#     return render(request, 'sam_api/entity_list.html', {'entities': all_opportunities})

# ====================================================================================================

# def fetch_opportunities(api_key, start_date, end_date, page_size=3, page=1, filters=[]): # page_size=1000
#     url = "https://api.sam.gov/opportunities/v2/search"
#     params = {
#         'api_key': api_key,
#         'postedFrom': start_date,
#         'postedTo': end_date,
#         'limit': page_size,
#         'offset': (page - 1) * page_size,
#     }

#     for filter_param in filters:
#         params.update(filter_param)
    
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         print(f"Response data: {data}")
#         if "opportunitiesData" in data:
#             opportunities = data["opportunitiesData"]
#             total_records = data["totalRecords"]
#             print(f"Fetched {len(opportunities)} opportunities (Page {page}).")
#             return opportunities, total_records
#         else:
#             print("No data found in the API response.")
#             return [], 0
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred while making the request: {e}")
#         print(f"Response content: {response.content}")
#         if response.status_code == 429:
#             print("API rate limit exceeded. Waiting for 60 seconds.")
#             return None, 0
#         return [], 0

# def fetch_all_opportunities(api_key, start_date, end_date, page_size=3, filters=[]): # page_size=1000
#     all_opportunities = []
#     page = 1
#     total_records = 0
#     while True:
#         opportunities, records_count = fetch_opportunities(api_key, start_date, end_date, page_size, page, filters)
#         if opportunities is None:
#             time.sleep(60)
#             continue
#         all_opportunities.extend(opportunities)
#         total_records = records_count
#         if len(opportunities) < page_size:
#             break
#         page += 1
#     return all_opportunities, total_records

# def save_opportunities_to_db(opportunities):
#     for opp in opportunities:
#         award = opp.get("award", {})
#         awardee = award.get("awardee", {})
#         location = awardee.get("location", {})
#         place_of_performance = opp.get("placeOfPerformance", {})
#         place_of_performance_city = place_of_performance.get("city", {})
#         place_of_performance_country = place_of_performance.get("country", {})

#         Opportunity.objects.update_or_create(
#             notice_id=opp['noticeId'],
#             defaults={
#                 "title": opp.get("title"),
#                 "solicitation_number": opp.get("solicitationNumber"),
#                 "department": opp.get("department"),
#                 "sub_tier": opp.get("subTier"),
#                 "office": opp.get("office"),
#                 "posted_date": opp.get("postedDate"),
#                 "opportunity_type": opp.get("type"),
#                 "base_type": opp.get("baseType"),
#                 "archive_type": opp.get("archiveType"),
#                 "archive_date": opp.get("archiveDate"),
#                 "naics_code": opp.get("naicsCode"),
#                 "classification_code": opp.get("classificationCode"),
#                 "active": opp.get("active"),
#                 "award_date": award.get("date"),
#                 "award_number": award.get("number"),
#                 "award_amount": award.get("amount"),
#                 "awardee_name": awardee.get("name"),
#                 "awardee_street_address": location.get("streetAddress"),
#                 "awardee_city": location.get("city", {}).get("name"),
#                 "awardee_state": location.get("state", {}).get("code"),
#                 "awardee_zip": location.get("zip"),
#                 "awardee_country": location.get("country", {}).get("code"),
#                 "awardee_ueiSAM": awardee.get("ueiSAM"),
#                 "point_of_contact_email": opp.get("pointOfContact", [{}])[0].get("email"),
#                 "point_of_contact_phone": opp.get("pointOfContact", [{}])[0].get("phone"),
#                 "point_of_contact_name": opp.get("pointOfContact", [{}])[0].get("fullName"),
#                 "description": opp.get("description"),
#                 "organization_type": opp.get("organizationType"),
#                 "office_zipcode": opp.get("officeAddress", {}).get("zipcode"),
#                 "office_city": opp.get("officeAddress", {}).get("city"),
#                 "office_state": opp.get("officeAddress", {}).get("state"),
#                 "office_country_code": opp.get("officeAddress", {}).get("countryCode"),
#                 "place_of_performance_street_address": place_of_performance.get("streetAddress"),
#                 "place_of_performance_city": place_of_performance_city.get("name"),
#                 "place_of_performance_state": place_of_performance.get("state", {}).get("code"),
#                 "place_of_performance_zip": place_of_performance.get("zip"),
#                 "place_of_performance_country": place_of_performance_country.get("code"),
#                 "ui_link": opp.get("uiLink"),
#                 "additional_info_link": opp.get("additionalInfoLink"),
#             },
#         )

# def fetch_opportunities_view(request):
#     api_key = env('API_KEY')
#     last_how_many_days = 30
#     start_date = (datetime.now() - timedelta(days=last_how_many_days)).strftime('%m/%d/%Y')
#     end_date = datetime.now().strftime('%m/%d/%Y')
#     filters = []  # Define any filters if needed
#     all_opportunities, total_records = fetch_all_opportunities(api_key, start_date, end_date, page_size=3, filters=filters)
#     save_opportunities_to_db(all_opportunities)
#     print(f"Total opportunities fetched and saved: {len(all_opportunities)} out of {total_records} records.")
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "entities", 
#         {
#             "type": "send_entities", 
#             "text": [opportunity.to_dict() for opportunity in all_opportunities],
#         }
#     )
#     return JsonResponse({'status': 'success'})

# def entity_list(request):
#     entities = Opportunity.objects.all()
#     return render(request, 'sam_api/entity_list.html', {'entities': entities})

# ====================================================================================================

def fetch_opportunities(api_key):
    url = "https://api.sam.gov/opportunities/v2/search"
    start_date = (datetime.now() - timedelta(days=30)).strftime("%m/%d/%Y")
    end_date = datetime.now().strftime("%m/%d/%Y")
    all_opportunities = []
    params = {
        'api_key': api_key,
        'postedFrom': start_date,
        'postedTo': end_date,
        'limit': 10,  # Fetch only one opportunity for now
    }

    # try:
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     data = response.json()
    #     opportunities = data.get("opportunitiesData", [])
    #     return opportunities
    # except requests.exceptions.RequestException as e:
    #     print(f"An error occurred while making the request: {e}")
    #     print(f"Response content: {response.content}")
    #     return []

    try:
        while True: 
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            opportunities = data.get("opportunitiesData", [])
            if not opportunities:
                break
            all_opportunities.extend(opportunities)
            params['page'] = data.get('next')
            if not params['page']:
                break
        return all_opportunities
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        print(f"Response content: {response.content}")
        return []

def parse_date(date_string):
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    return None

# def save_opportunities_to_db(opportunities):
#     for opp in opportunities:
#         Opportunity(
#             notice_id=opp['noticeId'],
#             title=opp.get("title"),
#             solicitation_number=opp.get("solicitationNumber"),
#             department=opp.get("department"),
#             sub_tier=opp.get("subTier"),
#             office=opp.get("office"),
#             posted_date=datetime.strptime(opp.get("postedDate", ""), "%m/%d/%Y") if opp.get("postedDate") else None,
#             opportunity_type=opp.get("type"),
#             base_type=opp.get("baseType"),
#             archive_type=opp.get("archiveType"),
#             archive_date=datetime.strptime(opp.get("archiveDate", ""), "%m/%d/%Y") if opp.get("archiveDate") else None,
#             naics_code=opp.get("naicsCode"),
#             classification_code=opp.get("classificationCode"),
#             active=opp.get("active"),
#             award_date=datetime.strptime(opp.get("award", {}).get("date", ""), "%m/%d/%Y") if opp.get("award", {}).get("date") else None,
#             award_number=opp.get("award", {}).get("number"),
#             award_amount=opp.get("award", {}).get("amount"),
#             awardee_name=opp.get("award", {}).get("awardee", {}).get("name"),
#             awardee_street_address=opp.get("award", {}).get("awardee", {}).get("location", {}).get("streetAddress"),
#             awardee_city=opp.get("award", {}).get("awardee", {}).get("location", {}).get("city", {}).get("name"),
#             awardee_state=opp.get("award", {}).get("awardee", {}).get("location", {}).get("state", {}).get("code"),
#             awardee_zip=opp.get("award", {}).get("awardee", {}).get("location", {}).get("zip"),
#             awardee_country=opp.get("award", {}).get("awardee", {}).get("location", {}).get("country", {}).get("code"),
#             awardee_ueiSAM=opp.get("award", {}).get("awardee", {}).get("ueiSAM"),
#             point_of_contact_email=opp.get("pointOfContact", [{}])[0].get("email"),
#             point_of_contact_phone=opp.get("pointOfContact", [{}])[0].get("phone"),
#             point_of_contact_name=opp.get("pointOfContact", [{}])[0].get("fullName"),
#             description=opp.get("description"),
#             organization_type=opp.get("organizationType"),
#             office_zipcode=opp.get("officeAddress", {}).get("zipcode"),
#             office_city=opp.get("officeAddress", {}).get("city"),
#             office_state=opp.get("officeAddress", {}).get("state"),
#             office_country_code=opp.get("officeAddress", {}).get("countryCode"),
#             place_of_performance_street_address=opp.get("placeOfPerformance", {}).get("streetAddress"),
#             place_of_performance_city=opp.get("placeOfPerformance", {}).get("city", {}).get("name"),
#             place_of_performance_state=opp.get("placeOfPerformance", {}).get("state", {}).get("code"),
#             place_of_performance_zip=opp.get("placeOfPerformance", {}).get("zip"),
#             place_of_performance_country=opp.get("placeOfPerformance", {}).get("country", {}).get("code"),
#             ui_link=opp.get("uiLink"),
#             additional_info_link=opp.get("additionalInfoLink"),
#         ).save()

def save_opportunities_to_db(opportunities):
    for opp in opportunities:
        notice_id = opp['noticeId']
        if not Opportunity.objects(notice_id=notice_id):
            award = opp.get("award", {}) or {}
            awardee_location = award.get("awardee", {}).get("location", {}) or {}
            point_of_contact = opp.get("pointOfContact", [{}])[0] or {}
            place_of_performance = opp.get("placeOfPerformance", {}) or {}
            Opportunity(
                notice_id=notice_id,
                title=opp.get("title"),
                solicitation_number=opp.get("solicitationNumber"),
                department=opp.get("department"),
                sub_tier=opp.get("subTier"),
                office=opp.get("office"),
                posted_date=parse_date(opp.get("postedDate", "")) if opp.get("postedDate") else None,
                opportunity_type=opp.get("type"),
                base_type=opp.get("baseType"),
                archive_type=opp.get("archiveType"),
                archive_date=parse_date(opp.get("archiveDate", "")) if opp.get("archiveDate") else None,
                naics_code=opp.get("naicsCode"),
                classification_code=opp.get("classificationCode"),
                active=opp.get("active"),
                award_date=parse_date(award.get("date", "")) if award.get("date") else None,
                award_number=award.get("number"),
                award_amount=award.get("amount"),
                awardee_name=award.get("awardee", {}).get("name"),
                awardee_street_address=awardee_location.get("streetAddress"),
                awardee_city=awardee_location.get("city", {}).get("name"),
                awardee_state=awardee_location.get("state", {}).get("code"),
                awardee_zip=awardee_location.get("zip"),
                awardee_country=awardee_location.get("country", {}).get("code"),
                awardee_ueiSAM=award.get("awardee", {}).get("ueiSAM"),
                point_of_contact_email=point_of_contact.get("email"),
                point_of_contact_phone=point_of_contact.get("phone"),
                point_of_contact_name=point_of_contact.get("fullName"),
                description=opp.get("description"),
                organization_type=opp.get("organizationType"),
                office_zipcode=opp.get("officeAddress", {}).get("zipcode"),
                office_city=opp.get("officeAddress", {}).get("city"),
                office_state=opp.get("officeAddress", {}).get("state"),
                office_country_code=opp.get("officeAddress", {}).get("countryCode"),
                place_of_performance_street_address=place_of_performance.get("streetAddress"),
                place_of_performance_city=place_of_performance.get("city", {}).get("name"),
                place_of_performance_state=place_of_performance.get("state", {}).get("code"),
                place_of_performance_zip=place_of_performance.get("zip"),
                place_of_performance_country=place_of_performance.get("country", {}).get("code"),
                ui_link=opp.get("uiLink"),
                additional_info_link=opp.get("additionalInfoLink"),
            ).save()

# def fetch_opportunities_view(request):
def fetch_opportunities_view(request):
    # api_key = request.POST.get("api_key")
    api_key = env("API_KEY")
    opportunities = fetch_opportunities(api_key)
    save_opportunities_to_db(opportunities)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "opportunity_updates",
        {
            "type": "opportunity.message",
            "message": "New opportunity fetched",
        },
    )
    # return redirect("entity_list") & JsonResponse({"status": "success"})
    # return redirect("entity_list")
    return JsonResponse({"status": "success"})

def entity_list(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'sam_api/entity_list.html', {'entities': opportunities})