import hello_analytics_api_v3_auth
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
import datetime
import segmentIds as si
import dimensions_and_metrics
import collectArguments as ca
import analytics_ids as ai
import site_to_dictionary as std
import datetime
from datetime import timedelta
from datetime import date
service = si.service
accounts = si.accounts
unwanted_analytics_profiles = [27262717,430920,28439349,32052112,26104474,32417137,35397371,32046401,755863,31204267,2788499,31963017,31960032,8201396,16884628]


def get_dates():
    dates = {}
    dates["start"] = (raw_input("Enter Start Date in form YYYY-MM-DD"))
    dates["end"] = (raw_input("Enter End Date in form YYYY-MM-DD"))
    if check_dates(dates.values()):
        return dates
    else:
        print "dates_invalid"
        return get_dates()


def check_dates(dates):
    are_dates_valid = False
    try:
        start_year = int(dates[0][0:4])
        start_month = int (dates[0][5:7])
        start_day = int (dates[0][8:10])
        end_year = int(dates[1][0:4])
        end_month = int (dates[1][5:7])
        end_day = int (dates[1][8:10])
        if (2007<start_year<=int(datetime.datetime.now().strftime('%Y')) and (0<start_month<13) and (0<start_day<32)):
            if (2007<end_year<=int(datetime.datetime.now().strftime('%Y')) and (0<end_month<13) and (0<end_day<32)):
                if (start_year < end_year or (start_year == end_year and (start_month<end_month or (start_month == end_month and start_day <= end_day)))):
                    are_dates_valid = True
        else:
            are_dates_valid = False
        return are_dates_valid
    except:
        are_dates_valid = False
        return are_dates_valid


def get_segments():
    segmentName = ''
    segmentList = []
    entries_incomplete = True
    while (entries_incomplete):
        segmentName = raw_input("Enter Segment Name, hit Enter for All visits and DONE when complete")
        if segmentName.upper() == "DONE":
            entries_incomplete = False
        else:
            try:
                segmentList.append(si.segments_Dictionary[segmentName])
            except (KeyError):
                print "Sorry, there was a problem with this segment name."
    return segmentList

def get_sites_for_query():
    sites = []
    sites_incomplete = True
    for items in site_name_to_true_webPropertyId.keys():
        print items
    while (sites_incomplete):
        user_input = (raw_input("Enter Preferred site, when complete type DONE, for all sites, type ALL"))
        if (user_input.upper() == "ALL"):
                      sites = []
                      for items in site_name_to_true_webPropertyId.keys():
                          sites.append(items)
                      break
        elif user_input.upper() == "DONE":
                      sites_incomplete = False
                      break
        else:
                      try:
                          site_name_to_true_webPropertyId[user_input]
                          sites.append(user_input)
                      except:
                          print "sorry, that was a problem with that site/input. Please try again."
    return sites

def  get_account_items():
    Account_Items_Site_To_id = {}
    for x in range (len(accounts.get('items'))):
        j = accounts.get('items')[x]['name']
        k = accounts.get('items')[x].get('id')
        if k not in unwanted_analytics_profiles:
            Account_Items_Site_To_id[j] = k
    return Account_Items_Site_To_id

def get_site_profiles():
    return get_account_items().keys()

def get_profile_ids():
    complete_profile_ids = get_account_items().values()
    for unwanted_id in unwanted_analytics_profiles:
        try:
            complete_profile_ids.remove(str(unwanted_id))
        except(ValueError):
            pass
    return complete_profile_ids

def get_webproperties():
    webproperties = []
    for x in profile_ids:
        webproperties.append(service.management().webproperties().list(accountId=x).execute())
    return webproperties

def get_website_uas():
    returnList = []
    for x in webproperties:
        for j in x['items']:
            if j['id'] in ai.ids:
                returnList.append(j)
    return returnList

def get_account_ids_to_websites():
    newDict = {}
    for x in range (len(webproperties)):
        for y in range (len((webproperties[x]['items']))):
            if webproperties[x]['items'][y]['id'] in ai.ids:
                newDict[webproperties[x]['items'][y]['id']]= webproperties[x]['items'][y]['name']
    return newDict


def get_account_ids_to_website_ids():
    newestDict = {}
    for x in webproperties:
            for y in range (len(x['items'])):
                    try:
                            if x['items'][y]['id'] in ai.ids:
                                    newestDict[x['items'][y]['accountId']].append(x['items'][y]['id'])
                    except:
                            if x['items'][y]['id'] in ai.ids:
                                    newestDict[x['items'][y]['accountId']] = [x['items'][y]['id']]
    return newestDict

def get_profile_list():
    profileList = []
    for x in range(len(profile_ids)):
        for y in range (len(account_ids_to_website_ids[profile_ids[x]])):
            profiles = service.management().profiles().list(
                accountId=profile_ids[x],
                webPropertyId=account_ids_to_website_ids[profile_ids[x]][y]).execute()
            profileList.append(profiles)
    return profileList

def get_site_name_to_true_webPropertyId():
    returnDict = {}
    for x in range(len(all_profiles)):
        returnDict[all_profiles[x].get('items')[0].get('name')] = all_profiles[x].get('items')[0].get('id')
    return returnDict

def get_websites_to_account_ids():
    return {v:k for k,v in account_ids_to_websites.items()}
    

def get_filters():
    return(raw_input("Enter Filter - (for advanced users only. If you are not an advanced user, please hit enter)"))
    

def get_results(service,profile_id,segment_id,date1,dimensionString,metricString):
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=date1,
        end_date=date1,
        dimensions=dimensionString,
        metrics=metricString).execute()


def get_arguments():
    dimensionString = ca.collectArguments(dimensions_and_metrics.dimensions)
    metricString = ca.collectArguments(dimensions_and_metrics.metrics)
    return [dimensionString,metricString]


profile_ids = get_profile_ids()
site_profiles = get_site_profiles()
account_items = get_account_items()
webproperties = get_webproperties()
account_ids_to_websites = get_account_ids_to_websites()
account_ids_to_website_ids = get_account_ids_to_website_ids()
all_profiles = get_profile_list()
site_name_to_true_webPropertyId = get_site_name_to_true_webPropertyId()
get_site_name_to_true_webPropertyId = get_site_name_to_true_webPropertyId()
websites_to_account_ids = get_websites_to_account_ids()
