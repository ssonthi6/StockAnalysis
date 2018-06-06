import urllib.request

functionR = "TIME_SERIES_INTRADAY"
symbolR = "MSFT"
intervalR = "1min"
apikeyR = "18ADUT83PYOCMCRU"


def savefileintraday(function, symbol, interval, apikey):
    return "https://www.alphavantage.co/query?" \
           "function=" + function + \
           "&symbol=" + symbol + \
           "&interval=" + interval + \
           "&apikey=" + apikey + \
           "&datatype=csv"

def savefiledaily(function, symbol, interval, apikey):
    return "https://www.alphavantage.co/query?" \
           "function=" + function + \
           "&symbol=" + symbol + \
           "&interval=" + interval + \
           "&apikey=" + apikey + \
           "&datatype=csv"


urllib.request.urlretrieve(savefileintraday(functionR, symbolR, intervalR, apikeyR), "file.csv")

# print(savefile(functionR, symbolR, intervalR, apikeyR))
