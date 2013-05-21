def previousYear(date):
    year = str(int(date[:4])-1)
    month = date[5:7]
    day = date[8:10]
    return year+'-'+month+'-'+day

def previousMonth(date):
    if int(date[5:7])>1:
        year = date[:4]
        month = str(int(date[5:7]-1))
    else:
        year = str(int(date[:4])-1)
        month = str(12)
    day = date[8:10]
    return year+'-'+month+'-'+day            
