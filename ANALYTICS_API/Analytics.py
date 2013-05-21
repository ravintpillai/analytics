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

service = hello_analytics_api_v3_auth.initialize_service()
accounts = service.management().accounts().list().execute()
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

def  get_account_items():
    Account_Items_Site_To_id = {}
    for x in range (len(accounts.get('items'))):
        j = accounts.get('items')[x]['name']
        k = accounts.get('items')[x].get('id')
        if j != 'groomingandbeauty.com':
            Account_Items_Site_To_id[j] = k
    return Account_Items_Site_To_id

def get_site_profiles():
    return get_account_items().keys()

def get_profile_ids():
    return get_account_items().values()

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

def get_results(service,profile_id,segment_id,date1,dimensionString,metricString):
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=date1,
        end_date=date1,
        segment=segment_id,
        ##Useful segment ids: 729961158 (ipad)
        dimensions=dimensionString,
        metrics=metricString).execute()

def get_segment():
    return si.segments_Dictionary[raw_input('enter segment')]

def get_site_name_to_webPropertyId():
    returnDict = {}
    for x in range(len(all_profiles)):
        returnDict[all_profiles[x].get('items')[0].get('name')] = all_profiles[x].get('items')[0].get('webPropertyId')
    return returnDict
    

def get_all_results():
    resultsList = []
    for x in range(len(all_profiles)):
        results = get_results(service,all_profiles[x].get('items')[0].get('id'),segment,today,'ga:hour','ga:visits')
        #print account_ids_to_websites[all_profiles[x].get('items')[0].get('webPropertyId')],'\n',results['rows'],'\n\n\n'
        resultsList.append(results)
    return resultsList

def get_all_results_dynamic(the_date,segment):
    resultsList = []
    for x in range(len(all_profiles)):
        results = get_results(service,all_profiles[x].get('items')[0].get('id'),segment,the_date,'ga:hour','ga:visits')
        #print account_ids_to_websites[all_profiles[x].get('items')[0].get('webPropertyId')],'\n',results['rows'],'\n\n\n'
        resultsList.append(results)
    return resultsList


def get_one_site_results(site):
    try:
        mysite = std.site_to_dictionary[site]
    except(KeyError):
        mysite = site
    results = get_results(service,site_name_to_true_webPropertyId[mysite],segment,today,'ga:hour','ga:visits')
    return results

def get_site_name_to_true_webPropertyId():
    returnDict = {}
    for x in range(len(all_profiles)):
        returnDict[all_profiles[x].get('items')[0].get('name')] = all_profiles[x].get('items')[0].get('id')
    return returnDict


def get_segmented_results():
    resultsList = []
    for x in range(len(std.segmentsList)):
        segment = si.segments_Dictionary[std.segmentsList[x]]
        resultsList.append((get_all_results(),std.segmentsList[x]))
    return resultsList

def get_segmented_results_dynamic(the_date):
    resultsList = []
    for x in range(len(std.segmentsList)):
        segment = si.segments_Dictionary[std.segmentsList[x]]
        resultsList.append((get_all_results_dynamic(the_date,segment),std.segmentsList[x]))
    return resultsList



def get_dates():
    dateList = []
    today = date.today()
    for x in range(5):
        dateList.append((today-timedelta(days=7*x)).strftime('%Y-%m-%d'))
    return dateList


def get_final_results():
    final_results_list = []
    for the_date in dates:
        our_results = get_segmented_results()
        final_results_list.append((our_results,the_date))
    return final_results_list
        
        

#segment = 1
#profile_ids are in account_ids_to_website_ids
profile_ids = get_profile_ids()
site_profiles = get_site_profiles()
account_items = get_account_items()
webproperties = get_webproperties()
account_ids_to_websites = get_account_ids_to_websites()
account_ids_to_website_ids = get_account_ids_to_website_ids()
all_profiles = get_profile_list()
#segment=get_segment()
#all_results = get_all_results()
site_name_to_true_webPropertyId = get_site_name_to_true_webPropertyId()
get_site_name_to_true_webPropertyId = get_site_name_to_true_webPropertyId()
#segmented_results = get_segmented_results()
dates = get_dates()
final_results = get_final_results()



#site_name_to_webPropertyId = get_site_name_to_webPropertyId()
#print account_ids_to_website_ids




#webpropties[n]['items'][k]['name'] corresponds to site_profiles
#where n defines which webproperty and k defines which site within that webproperty

#one_site_results = get_one_site_results(raw_input('enter site').upper())






