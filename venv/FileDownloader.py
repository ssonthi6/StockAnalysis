import urllib.request

symboltest = "MSFT"
intervaltest = "1min"
apikey = "18ADUT83PYOCMCRU"


def savefileintraday(symbol, interval):
    return "https://www.alphavantage.co/query?" \
           "function=TIME_SERIES_INTRADAY" \
           "&symbol=" + symbol + \
           "&interval=" + interval + \
           "&apikey=18ADUT83PYOCMCRU" \
           "&datatype=csv"

def savefiledaily(symbol):
    return "https://www.alphavantage.co/query?" \
           "function=TIME_SERIES_DAILY" \
           "&symbol=" + symbol + \
           "&apikey=18ADUT83PYOCMCRU" \
           "&datatype=csv"


urllib.request.urlretrieve(savefileintraday(symboltest, intervaltest), "file.csv")

# print(savefile(functionR, symbolR, intervalR, apikeyR))
