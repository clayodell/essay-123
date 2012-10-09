from datetime import datetime

def getTimeInDaysMinutesSeconds(seconds):
    d = dict()
    if(seconds < 60):
        d['num'] = seconds
        if(d['num'] <= 1):
            d['metric'] = 'second'
        else:
            d['metric'] = 'seconds'
        return d
    elif (seconds >= 60 and seconds < 3600):
        d['num'] = seconds / 60
        if(d['num'] <= 1):
            d['metric'] = 'minute'
        else:
            d['metric'] = 'minutes'
        return d
    elif (seconds >= 3600 and seconds < 86400):
        d['num'] = seconds / 3600
        if(d['num'] <= 1):
            d['metric'] = 'hour'
        else:
            d['metric'] = 'hours'
        return d
    elif (seconds >= 86400):
        d['metric'] = 'days'
        d['num'] = seconds / 86400
        if(d['num'] <= 1):
            d['metric'] = 'day'
        else:
            d['metric'] = 'days'
        return d

def getSecondsFromNow(otherDate):
    d1 = datetime.now()
    d2 = otherDate
    d3 = d1 - d2
    return d3.seconds + d3.days * 86400