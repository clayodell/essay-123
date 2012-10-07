
class Helpers():
    
    def getTimeInDaysMinutesSeconds(self,seconds):
        d = dict()
        if(seconds < 60):
            d['seconds'] = seconds
            return d
        elif (seconds >= 60 and seconds < 3600 ):
            d['minutes'] = abs(seconds/60)
            return d
        elif (seconds >= 3600 and seconds < 86400):
            d['hours'] = seconds/3600
            return d
        elif (seconds >= 86400):
            d['days'] = seconds/86400
            return d
        