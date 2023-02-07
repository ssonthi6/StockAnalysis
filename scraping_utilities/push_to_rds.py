import os
import numpy as np
from scipy.stats import norm
import math
import datetime
import glob
import psycopg2

now = datetime.datetime.now()

def bsm_no_div(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    d_2 = d_1 - vol * np.power(T, 0.5)
    nd_1 = norm.cdf(d_1)
    nd_2 = norm.cdf(d_2)
    call = s_0 * nd_1 - np.exp(-r_f * T) * k * nd_2
    put = call + k * np.exp(-r_f * T) - s_0
    return (call, put)

def bsm_yield_div(k, s_0, r_f, vol, T, delta):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f - delta + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    d_2 = d_1 - vol * np.power(T, 0.5)
    nd_1 = norm.cdf(d_1)
    nd_2 = norm.cdf(d_2)
    call = s_0 * np.exp(-delta * T) * nd_1 - np.exp(-r_f * T) * k * nd_2
    put = np.exp(-r_f * T) * k * (1-nd_2) - s_0 * np.exp(-delta * T) * (1-nd_1)
    return (call, put)

def delta_call(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    return d_1
    
def delta_put(k, s_0, r_f, vol, T):
    return delta_call(k, s_0, r_f, vol, T) - 1
    
def vega(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    n_prime = np.exp(-np.power(d_1,2)/2)/(np.power(2*math.pi, 0.5))
    return s_0 * np.power(T, 0.5) * n_prime
    
def theta_call(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    d_2 = d_1 - vol * np.power(T, 0.5)
    n_prime = np.exp(-np.power(d_1,2)/2)/(np.power(2*math.pi, 0.5))
    theta = -(s_0 * n_prime * vol)/(2 * np.power(T,0.5)) - (r_f * k * np.exp(-r_f * T) * norm.cdf(d_2))
    return theta
    
def theta_put(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    d_2 = d_1 - vol * np.power(T, 0.5)
    n_prime = np.exp(-np.power(d_1,2)/2)/(np.power(2*math.pi, 0.5))
    theta = -(s_0 * n_prime * vol)/(2 * np.power(T,0.5)) + (r_f * k * np.exp(-r_f * T) * norm.cdf(-d_2))
    return theta
    
def rho_call(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    return k * T * np.exp(-r_f * T) * norm.cdf(d_1)
    
def rho_put(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    return -k * T * np.exp(-r_f * T) * norm.cdf(-d_1)
    
def gamma(k, s_0, r_f, vol, T):
    if vol == 0.0:
        vol = 10**-10
    d_1 = (np.log(s_0/k) + T*(r_f + np.power(vol, 2)/2)) / (vol * np.power(T, 0.5))
    n_prime = np.exp(-np.power(d_1,2)/2)/(np.power(2*math.pi, 0.5))
    return n_prime / (s_0 * vol * np.power(T, 0.5))

def iv_call(k, s_0, r_f, T, call):
    vol = 0.0
    power = -1
    bsm_prev = (0.0, 0.0)
    while vol < 5 and power >= -5:
        bsm_prev = bsm_no_div(k, s_0, r_f, vol, T)
        if bsm_prev[0] > call:
            vol = vol - 10**power
            power = power - 1
        else:
            vol = vol + 10**power
    return vol

def iv_put(k, s_0, r_f, T, put):
    vol = 0.0
    power = -1
    bsm_prev = (0.0, 0.0)
    while vol < 5 and power >= -5:
        bsm_prev = bsm_no_div(k, s_0, r_f, vol, T)
        if bsm_prev[1] > put:
            vol = vol - 10**power
            power = power - 1
        else:
            vol = vol + 10**power
    return vol

def iv_call_div(k, s_0, r_f, T, delta, call):
    vol = 0.0
    power = -1
    bsm_prev = (0.0, 0.0)
    while vol < 5 and power >= -5:
        bsm_prev = bsm_yield_div(k, s_0, r_f, vol, T, delta)
        if bsm_prev[0] > call:
            vol = vol - 10**power
            power = power - 1
        else:
            vol = vol + 10**power   
    return vol

def iv_put_div(k, s_0, r_f, T, delta, put):
    vol = 0.0
    power = -1
    bsm_prev = (0.0, 0.0)
    while vol < 5 and power >= -5:
        bsm_prev = bsm_yield_div(k, s_0, r_f, vol, T, delta)
        if bsm_prev[1] > put:
            vol = vol - 10**power
            power = power - 1
        else:
            vol = vol + 10**power    
    return vol


ENDPOINT="options-db.calen2rzlvid.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="us-east-1"
DBNAME="postgres"

fp = "/Users/sohamsonthi/Downloads/opt/SPY/2023-01-24_23:18:42/1676592000.txt"
tot_path = "/home/optn/Downloads/SPY/**/*.txt"
files = glob.glob(tot_path, recursive=True)
files.remove("/home/optn/Downloads/SPY/exp.txt")
print(len(files))

ticker = tot_path.split("/")[-3]

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password="QWERasdzx1", sslrootcert="SSLCERTIFICATE")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS {} (
            pull_date TIMESTAMP NOT NULL,
            is_call BOOL NOT NULL,
            expiry TIMESTAMP NOT NULL,
            strike FLOAT NOT NULL,
            stock_price FLOAT NOT NULL,
            bid FLOAT,
            ask FLOAT,
            open_interest INT,
            implied_vol FLOAT,
            theta FLOAT,
            delta FLOAT,
            gamma FLOAT,
            vega FLOAT,
            rho FLOAT
        );
        """.format(ticker))
    conn.commit()
except Exception as e:
    print("Database connection failed due to {}".format(e))

header = """INSERT INTO {} (pull_date, is_call, expiry, strike, stock_price, bid, ask,
        open_interest, implied_vol, theta, delta, gamma, vega, rho)""".format(ticker)

for fp in files:
    opt = []
    with open(fp, "r") as f:
        opt = f.read().split("\n")

    stock_price = float(opt[0].replace(",",""))

    index = [idx for idx, s in enumerate(opt) if 'Call' in s][0]
    trimmed = opt[index:]
    put_i = [idx for idx, s in enumerate(trimmed) if 'Put' in s][0]

    # LastPrice Bid Ask Change %Change Volume OpenInterest ImpliedVolatility'
    calls = trimmed[3:put_i]
    puts = trimmed[put_i+3:]

    date_time = fp.split("/")[-2]
    current_time = datetime.datetime.strptime(date_time, "%Y-%m-%d_%H:%M:%S")

    expiry = int(fp.split("/")[-1].split(".")[0])
    exp_time = (datetime.datetime.utcfromtimestamp(expiry)+datetime.timedelta(hours=16))
    seconds_in_day = 24 * 60 * 60
    t = (exp_time - current_time).total_seconds() / seconds_in_day
    if t <= 0:
        t = 0.1
    r_f = 0.035

    for call in calls:
        split = call.split(" ")
        last_trade = split[1]
        strike = float(split[4].replace(",",""))
        bid = float(split[6].replace(",",""))
        ask = float(split[7].replace(",",""))
        open_interest = split[-2].replace(",","")
        if open_interest == "-":
            open_interest = 1
        open_interest = int(open_interest)
        is_call = True
        option_price = ask
        iv = iv_call(strike, stock_price, r_f, t/365, option_price)
        if iv <= 0:
            iv = 0.001
        theta = theta_call(strike, stock_price, r_f, iv, t/365)
        delta = delta_call(strike, stock_price, r_f, iv, t/365)
        gam = gamma(strike, stock_price, r_f, iv, t/365)
        veg = vega(strike, stock_price, r_f, iv, t/365)
        rho = rho_call(strike, stock_price, r_f, iv, t/365)
        try:
            cur.execute(header + """ VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                        (current_time, is_call, exp_time, strike, stock_price, bid, ask, open_interest, iv, theta,
                        delta, gam, veg, rho))
            conn.commit()
        except Exception as e:
            print("Database connection failed due to {}".format(e))

    for put in puts:
        split = put.split(" ")
        last_trade = split[1]
        strike = float(split[4].replace(",",""))
        bid = float(split[6].replace(",",""))
        ask = float(split[7].replace(",",""))
        open_interest = split[-2].replace(",","")
        if open_interest == "-":
            open_interest = 1
        open_interest = int(open_interest)
        is_call = False
        option_price = ask
        iv = iv_put(strike, stock_price, r_f, t/365, option_price)
        if iv <= 0:
            iv = 0.001
        theta = theta_put(strike, stock_price, r_f, iv, t/365)
        delta = delta_put(strike, stock_price, r_f, iv, t/365)
        gam = gamma(strike, stock_price, r_f, iv, t/365)
        veg = vega(strike, stock_price, r_f, iv, t/365)
        rho = rho_put(strike, stock_price, r_f, iv, t/365)
        try:
            cur.execute(header + """ VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                        (current_time, is_call, exp_time, strike, stock_price, bid, ask, open_interest, iv, theta,
                        delta, gam, veg, rho))
            conn.commit()
        except Exception as e:
            print("Database connection failed due to {}".format(e))

conn.close()
print(datetime.datetime.now() - now)
