myFile = open("G:\\.Customer Insight\\analytics_ids.csv")
def get_ids():
    myList= []
    for line in myFile:
        myList.append(line)
    for x in range(len(myList)):
        myList[x] = myList[x].strip(' \n')
    return myList

ids = get_ids()
myFile.close()
