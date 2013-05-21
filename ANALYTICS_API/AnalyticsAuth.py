import hello_analytics_api_v3_auth
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
import dateMethods
import collectArguments

service = hello_analytics_api_v3_auth.initialize_service()
accounts = service.management().accounts().list().execute()

class Arguments(object):
    def __init__(self,dateList,dimensionList,metricList,filters,segment):
        self.dateList = dateList
        self.dimenstionList = dimensionList
        self.metricList = metricList
        self.filters = filters
        self.segment = segment
    def dimensionList(self):
        return self.dimensionList
    def metricList(self):
        return self.metricList
    def filters(self):
        return self.filters
    def segments(self):
        return self.segment
    def dateList(self):
        return self.dateList
    def previousYearDateList(self):
        PYstartDate = dateMethods.previousYear(dateList[0])
        PYendDate = dateMethods.previousYear(dateList[1])
    def previousMonthDateList(self):
        PYstartDate = dateMethods.previousMonth(dateList[0])
        PYendDate = dateMethods.previousMonth(dateList[1])
    def previousDayDateList(self):
        PYstartDate = dateMethods.previousDay(dateList[0])
        PYendDate = dateMethods.previousDay(dateList[1])            

class Results(object):
    def __init__(self,arguments):
        self.arguments = arguments
        self.results = service.data().ga().get(
            ids = 'ga:' + get_first_profile_id(service,accounts,0,0)[0],
            start_date = arguments.dateList()[0],
            end_date = arguments.dateList()[1],
            segment = arguments.segments(),
            dimensions = playing.dimensionString,
            metrics = playing.metricString
        ).execute()

def get_first_profile_id(service,accounts,accountProfiles,x):
  # Get a list of all Google Analytics accounts for this user
  ##print service.management().accounts().list()

  if accounts.get('items'):
    # Get the first Google Analytics account
    firstAccountId = accounts.get('items')[accountProfiles].get('id')
##    print "firstAccountID \t%s" %str(firstAccountId)

    # Get a list of all the Web Properties for the first account
    webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()
    try:
      if webproperties.get('items'):
        # Get the first Web Property ID
        firstWebpropertyId = webproperties.get('items')[x].get('id')

        # Get a list of all Profiles for the first Web Property of the first Account
        profiles = service.management().profiles().list(
            accountId=firstAccountId,
            webPropertyId=firstWebpropertyId).execute()

        if profiles.get('items'):
          # return the first Profile ID
          return [profiles.get('items')[0].get('id'),firstWebpropertyId]
    except:
      if webproperties.get('items'):
  # Get the first Web Property ID
        firstWebpropertyId = webproperties.get('items')[0].get('id')

  # Get a list of all Profiles for the first Web Property of the first Account
        profiles = service.management().profiles().list(
            accountId=firstAccountId,
            webPropertyId=firstWebpropertyId).execute()

        if profiles.get('items'):
          # return the first Profile ID
          return [profiles.get('items')[0].get('id'),firstWebpropertyId]
  return [None,None]

def countWebProperties(service,accounts,accountProfiles):
  firstAccountId = accounts.get('items')[accountProfiles].get('id')
  webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()
  length = len(webproperties.get('items'))
  ##print len(webproperties.get('items'))
  return length

