import Analytics_Methods as AM
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



profile_ids = AM.get_profile_ids()
site_profiles = AM.get_site_profiles()
account_items = AM.get_account_items()
webproperties = AM.get_webproperties()
account_ids_to_websites = AM.get_account_ids_to_websites()
account_ids_to_website_ids = AM.get_account_ids_to_website_ids()
all_profiles = AM.get_profile_list()
site_name_to_true_webPropertyId = AM.get_site_name_to_true_webPropertyId()
get_site_name_to_true_webPropertyId = AM.get_site_name_to_true_webPropertyId()
dates = AM.get_dates()
final_results = AM.get_final_results()
#write_to_file()
