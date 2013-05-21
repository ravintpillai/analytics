#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import io
# import the Auth Helper class
import hello_analytics_api_v3_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
service = hello_analytics_api_v3_auth.initialize_service()
accounts = service.management().accounts().list().execute()


def main(argv):
  funDict = {'':'-1','UK':'470502913'}

  # Step 1. Get an analytics service object.
  segment_id = 'gaid::-1'
  try:
    profiles = service.management().segments().list().execute()

  except TypeError, error:
  # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)
    profiles = {'items':'hi'}

  except HttpError, error:
  # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
         (error.resp.status, error._get_reason()))
    profiles = {'items':'ho'}

  for segment in profiles.get('items', []):
    funDict[segment.get('name')] = segment.get('id')

  return funDict

segments_Dictionary = main(sys.argv)
