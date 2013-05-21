import dimensions_and_metrics
import segmentIds

def collectArguments(argumentType):
    outputString = ''
    outputNameList = []
    helperBoolean = True
    while helperBoolean:
      if argumentType == dimensions_and_metrics.dimensions:
          outputName = raw_input('Enter your preferred dimensions, once you are done type DONE')
      elif argumentType == dimensions_and_metrics.metrics:
          outputName = raw_input('Enter your preferred metrics, once you are done type DONE')
      else:
          print "This is not an argument Type I Recognize"
      if outputName == 'DONE':
        helperBoolean = False
      else:
        try:
            outputName= argumentType[outputName]
            outputNameList.append(outputName)
        except(KeyError):
            print "sorry, I didn't understand that argument. Please Start Again"
            return collectArguments(argumentType)
    for x in range (0,len(outputNameList)):
      outputString += outputNameList[x]
      if x != len(outputNameList)-1:
        outputString += ','
    return outputString

def getDates():
    date1 = raw_input('Enter Start Date as YYYY-MM-DD ')
    date2 = raw_input('Enter End Date as YYYY-MM-DD ')
    return [date1,date2]

def getFilename():
    filename = 'g:\\.Customer Insight\\#AnalyticsAPI\\'+ raw_input('Enter preferred filename')+'.txt'
    return filename

def collectLists(argument):
    if argument == '':
        returnList = []
    else:
        returnList = argument.split(',')
    return returnList

def getSegments():
    segmentName = raw_input('Please Enter your preferred Segment Name (Hit Enter for All Visits)\n')
    try:
        segment_id = 'gaid::'+segmentIds.segments_Dictionary[segmentName]
    except:
        print "Oh dear, That Segment doesn't exist. Please try again or hit enter for no segments"
        segment_id = 'gaid::'+segmentIds.segments_Dictionary[segmentName]
    return segment_id

def getFilters():
    filterName = raw_input('Enter Filter, for no filters hit enter')
    return filterName
    
