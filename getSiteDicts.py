import getDataFromTables as gd

def totalrev(site):
    ## Getting list of lists corresponding to table rows (See SQL query)
    results = gd.results
    todayRev = {}
    previousRev = {}
    dayList = []
    for x in results:
        ## Filtering for site passed in as parameter
            if site in x:
                ## Getting all (number of days since 1-1-2000) contained in results
                    if x[4] not in dayList:
                            dayList.append(x[4])
                            
    today = max(dayList)
    for x in results:
            if site in x:
                ## Add the revenue to the appropriate list (aggregating all previous day's revenue).
                    if x[4] == today:
                            todayRev[x[2]] = x[1]
                    else:
                            try:
                                    previousRev[x[2]] += x[1]
                            except:
                                    previousRev[x[2]] = x[1]
    return (todayRev,previousRev)

def getSiteList():
    siteList = []
    for x in gd.results:
        if x[0] not in siteList:
            siteList.append(x[0])
    return siteList

def getSiteDicts():
    returnDict = {}
    for sites in getSiteList():
        returnDict[sites] = totalrev(sites)
    return returnDict

Data = getSiteDicts()
    
