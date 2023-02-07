#! /usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import csv
import argparse
import time
import os

parser = argparse.ArgumentParser()

parser.add_argument("--ticker", "-t")

args = parser.parse_args()

ticker = args.ticker

timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")

cwd = os.path.dirname(os.path.realpath(__file__))
exp_dir = "{}/exp.txt".format(ticker)
save_dir = "{t}/{q}/".format(t=ticker, q=timestamp)

if not os.path.exists(os.path.join(cwd, save_dir)):
    os.makedirs(os.path.join(cwd, save_dir))

chrome_options= Options()
chrome_options.add_argument("--headless")
# ser = Service(r"/home/optn/Downloads/chromedriver/chromedriver")
# driver = webdriver.Chrome(service=ser,
                        # options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

f = open(os.path.join(cwd, exp_dir))
dates = f.read().split("\n")


for d in dates:
    # Set the URL of the Yahoo Finance options page
    url = "https://finance.yahoo.com/quote/{t}/options?p={t}&date={dat}".format(t=ticker, dat=d)

    # Initialize the webdriver
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    # Wait for the pop-up to appear and then close it
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"myLightboxContainer\"]/section/button[2]")))
        popup = driver.find_element(By.XPATH, "//*[@id=\"myLightboxContainer\"]/section/button[2]")
        popup.click()
    except:
        print("No popup found")

    # Wait for the options table to load
    wait.until(EC.presence_of_element_located((By.ID, "mrt-node-Col1-1-OptionContracts")))

    # Find the options table
    options_table = driver.find_element(By.ID, "mrt-node-Col1-1-OptionContracts")
    
    stock_price = driver.find_element(By.XPATH, "//*[@id=\"quote-header-info\"]/div[3]/div[1]/div[1]/fin-streamer[1]")

    with open(os.path.join(cwd, save_dir, "{}.txt".format(d)), 'w+', newline='') as f:
        f.write(stock_price.text + "\n" + options_table.text)

    print("written " + str(d))

# Close the webdriver
driver.close()

print("finished writing")
