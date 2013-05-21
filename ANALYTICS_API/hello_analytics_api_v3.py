#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# import the Auth Helper class
import hello_analytics_api_v3_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

def main(argv):
  # Step 1. Get an analytics service object.
  service = hello_analytics_api_v3_auth.initialize_service()
  for sites in range (12):
    try:
      # Step 2. Get the user's first profile ID.
      profile_id = get_first_profile_id(service,sites)
      print "profileID \t%s" %str(profile_id)

      if profile_id:
        # Step 3. Query the Core Reporting API.
        results = get_results(service, profile_id)
        #print "I got the results"

        # Step 4. Output the results.
        print_results(results)
       #print "I printed the results"

    except TypeError, error:
      # Handle errors in constructing a query.
      print ('There was an error in constructing your query : %s' % error)

    except HttpError, error:
      # Handle API errors.
      print ('Arg, there was an API error : %s : %s' %
             (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
      # Handle Auth errors.
      print ('The credentials have been revoked or expired, please re-run '
             'the application to re-authorize')

def get_first_profile_id(service,sites):
  # Get a list of all Google Analytics accounts for this user
  ##print "I am trying to get first profile ID"
  accounts = service.management().accounts().list().execute()
  ##print service.management().accounts().list()
  ##if sites == 0:
   ## print accounts.get('items')[sites]
   ## print accounts.get('items')[sites+1]
  ##print accounts.get('items')[1]
  ##print accounts.get('items')[1].get('id')

  if accounts.get('items'):
    # Get the first Google Analytics account
    firstAccountId = accounts.get('items')[sites].get('id')
    print "firstAccountID \t%s" %str(firstAccountId)

    # Get a list of all the Web Properties for the first account
    webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()

    if webproperties.get('items'):
      # Get the first Web Property ID
      firstWebpropertyId = webproperties.get('items')[0].get('id')

      # Get a list of all Profiles for the first Web Property of the first Account
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        # return the first Profile ID
        return profiles.get('items')[0].get('id')
  return None


def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2012-07-31',
      ##The start date dates range is hard coded here
      ##We have to change this so it becomes an input parameter
      end_date='2012-07-31',
      ##The end date is also hard coded in
      ##Change this to be an input parameter
      ##If you run out of ideas, read the start date off a txt file
      ##And then have the user change the text file before running
      ##the program
      metrics='ga:visits').execute()

def print_results(results):
  # Print data nicely for the user.
  #print results
  if results:
    print 'Profile:\t%s' % results.get('profileInfo').get('profileName')
    print 'Total Visits:\t%s' % results.get('rows')[0][0]

  else:
    print 'No results found'

##if __name__ == '__main__':
main(sys.argv)
