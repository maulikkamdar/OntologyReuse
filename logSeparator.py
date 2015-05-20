import os
import sys
import datetime
import time


logFile = open("full_bp_protege.log")
logLines = logFile.readlines()
logFile.close()

loggedIps = {}
loggedTimes = {}
folder = "ConIPlogsessions/"
month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

for i in range(len(logLines)):
    logParams = logLines[i].strip().split()
    if "concepts" in logParams[6]:
        toPrintParts = logParams[6].split("?conceptid=")
        if len(toPrintParts) > 1:
            toPrint = toPrintParts[1].split("&apikey")[0]
        else:
            continue
    elif "path" in logParams[6]:
        toPrintParts = logParams[6].split("?source=")
        if len(toPrintParts) > 1:
            toPrint = toPrintParts[1].split("&apikey")[0]
        else:
            continue
    else:
        continue

    print toPrint

   
    strDate = logParams[3][1:len(logParams[3])]
    #print strDate
    a = strDate.split(":")
    date = a[0].split("/")
    now = datetime.datetime(int(date[2]), month[date[1]], int(date[0]), int(a[1]), int(a[2]), int(a[3]))
    #print now
    timestamp = time.mktime(now.timetuple())
   

    if logParams[0] in loggedIps:
        loggedIps[logParams[0]]["count"] = loggedIps[logParams[0]]["count"] + 1
        #loggedIps[logParams[0]]["text"] = loggedIps[logParams[0]]["text"] + logLines[i]
        sptime = timestamp - loggedIps[logParams[0]]["prevtime"]
        loggedIps[logParams[0]]["prevtime"] = timestamp
        with open(folder + logParams[0], "a") as indLogFile:
            indLogFile.write(str(sptime) + "\t" + str(now) + "\t" + toPrint + "\n")
            indLogFile.close()
    else:
        loggedIps[logParams[0]] = {"count": 1, "prevtime": timestamp}
        indLogFile = open(folder + logParams[0], "w+")
        sptime = timestamp - loggedIps[logParams[0]]["prevtime"]
        indLogFile.write(str(sptime) + "\t" + str(now) + "\t" + toPrint + "\n")
        indLogFile.close()
        #print logParams[0]

'''for key in loggedIps:
    print key + "-" + str(loggedIps[key]["count"])
    indLogFile = open("IPlogsessions/" + key, "w+")
    indLogFile.write(loggedIps[key]["text"])
    indLogFile.close()
'''
    

