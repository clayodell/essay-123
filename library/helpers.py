from datetime import datetime

def getTimeInDaysMinutesSeconds(seconds):
    d = dict()
    if(seconds < 60):
        d['metric'] = 'seconds'
        d['num'] = seconds
        return d
    elif (seconds >= 60 and seconds < 3600):
        d['metric'] = 'minutes'
        d['num'] = seconds / 60
        return d
    elif (seconds >= 3600 and seconds < 86400):
        d['metric'] = 'hours'
        d['num'] = seconds / 3600
        return d
    elif (seconds >= 86400):
        d['metric'] = 'days'
        d['num'] = seconds / 86400
        return d

def getSecondsFromNow(otherDate):
    d1 = datetime.now()
    d2 = otherDate
    d3 = d1 - d2
    return d3.seconds