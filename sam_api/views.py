import requests
from django.shortcuts import render
from django.http import JsonResponse
import environ
from datetime import datetime, timedelta
from .models import Opportunity
import time

# Create your views here.

env = environ.Env()

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

def fetch_opportunities(api_key, start_date, end_date, page_size=1000, page=1, filters=[]):
    url = "https://api.sam.gov/opportunities/v2/search"
    params = {
        'api_key': api_key,
        'postedFrom': start_date,
        'postedTo': end_date,
        'limit': page_size,
        'offset': (page - 1) * page_size,
    }

    for filter_param in filters:
        params.update(filter_param)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Response data: {data}")
        if "opportunitiesData" in data:
            opportunities = data["opportunitiesData"]
            total_records = data["totalRecords"]
            print(f"Fetched {len(opportunities)} opportunities (Page {page}).")
            return opportunities, total_records
        else:
            print("No data found in the API response.")
            return [], 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        print(f"Response content: {response.content}")
        if response.status_code == 429:
            print("API rate limit exceeded. Waiting for 60 seconds.")
            return None, 0
        return [], 0

def fetch_all_opportunities(api_key, start_date, end_date, page_size=1000, filters=[]):
    all_opportunities = []
    page = 1
    total_records = 0
    while True:
        opportunities, records_count = fetch_opportunities(api_key, start_date, end_date, page_size, page, filters)
        if opportunities is None:
            time.sleep(60)
            continue
        all_opportunities.extend(opportunities)
        total_records = records_count
        if len(opportunities) < page_size:
            break
        page += 1
    return all_opportunities, total_records

def save_opportunities_to_db(opportunities):
    for opp in opportunities:
        award = opp.get("award", {})
        awardee = award.get("awardee", {})
        location = awardee.get("location", {})
        place_of_performance = opp.get("placeOfPerformance", {})
        place_of_performance_city = place_of_performance.get("city", {})
        place_of_performance_country = place_of_performance.get("country", {})

        Opportunity.objects.update_or_create(
            notice_id=opp['noticeId'],
            defaults={
                "title": opp.get("title"),
                "solicitation_number": opp.get("solicitationNumber"),
                "department": opp.get("department"),
                "sub_tier": opp.get("subTier"),
                "office": opp.get("office"),
                "posted_date": opp.get("postedDate"),
                "opportunity_type": opp.get("type"),
                "base_type": opp.get("baseType"),
                "archive_type": opp.get("archiveType"),
                "archive_date": opp.get("archiveDate"),
                "naics_code": opp.get("naicsCode"),
                "classification_code": opp.get("classificationCode"),
                "active": opp.get("active"),
                "award_date": award.get("date"),
                "award_number": award.get("number"),
                "award_amount": award.get("amount"),
                "awardee_name": awardee.get("name"),
                "awardee_street_address": location.get("streetAddress"),
                "awardee_city": location.get("city", {}).get("name"),
                "awardee_state": location.get("state", {}).get("code"),
                "awardee_zip": location.get("zip"),
                "awardee_country": location.get("country", {}).get("code"),
                "awardee_ueiSAM": awardee.get("ueiSAM"),
                "point_of_contact_email": opp.get("pointOfContact", [{}])[0].get("email"),
                "point_of_contact_phone": opp.get("pointOfContact", [{}])[0].get("phone"),
                "point_of_contact_name": opp.get("pointOfContact", [{}])[0].get("fullName"),
                "description": opp.get("description"),
                "organization_type": opp.get("organizationType"),
                "office_zipcode": opp.get("officeAddress", {}).get("zipcode"),
                "office_city": opp.get("officeAddress", {}).get("city"),
                "office_state": opp.get("officeAddress", {}).get("state"),
                "office_country_code": opp.get("officeAddress", {}).get("countryCode"),
                "place_of_performance_street_address": place_of_performance.get("streetAddress"),
                "place_of_performance_city": place_of_performance_city.get("name"),
                "place_of_performance_state": place_of_performance.get("state", {}).get("code"),
                "place_of_performance_zip": place_of_performance.get("zip"),
                "place_of_performance_country": place_of_performance_country.get("code"),
                "ui_link": opp.get("uiLink"),
                "additional_info_link": opp.get("additionalInfoLink"),
            },
        )

def fetch_opportunities_view(request):
    api_key = env('API_KEY')
    last_how_many_days = 30
    start_date = (datetime.now() - timedelta(days=last_how_many_days)).strftime('%m/%d/%Y')
    end_date = datetime.now().strftime('%m/%d/%Y')
    filters = []  # Define any filters if needed
    all_opportunities, total_records = fetch_all_opportunities(api_key, start_date, end_date, page_size=1000, filters=filters)
    save_opportunities_to_db(all_opportunities)
    print(f"Total opportunities fetched and saved: {len(all_opportunities)} out of {total_records} records.")
    return JsonResponse({'success': True})

def entity_list(request):
    entities = Opportunity.objects.all()
    return render(request, 'sam_api/entity_list.html', {'entities': entities})