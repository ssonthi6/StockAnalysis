#! /usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("--ticker", "-t")

args = parser.parse_args()

ticker = args.ticker

cwd = os.path.dirname(os.path.realpath(__file__))
save_dir = "{}/".format(ticker)

if not os.path.exists(os.path.join(cwd, save_dir)):
    os.makedirs(os.path.join(cwd, save_dir))

# Set the URL of the Yahoo Finance options page
url = "https://finance.yahoo.com/quote/{t}/options?p={t}".format(t=ticker)

chrome_options= Options()
chrome_options.add_argument("--headless")
#ser = Service(r"/home/optn/Downloads/chromedriver/chromedriver")
#driver = webdriver.Chrome(service=ser, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print("initialized page")

wait = WebDriverWait(driver, 10)
# Wait for the pop-up to appear and then close it
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"myLightboxContainer\"]/section/button[2]")))
    popup = driver.find_element(By.XPATH, "//*[@id=\"myLightboxContainer\"]/section/button[2]")
    popup.click()
except:
    print("No popup found")
    
# Wait for the options table to load
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"Col1-1-OptionContracts-Proxy\"]/section/div/div[1]/select")))

# Find the options table
date_tables = driver.find_element(By.XPATH, "//*[@id=\"Col1-1-OptionContracts-Proxy\"]/section/div/div[1]/select")

# Get the rows of the options table
rows = date_tables.find_elements(By.TAG_NAME, "option")

dates = []
# Iterate through the rows and print the data
for row in rows:
    dates.append(row.get_attribute("value"))

# Close the webdriver
driver.close()

print("driver closed")

with open(os.path.join(cwd, save_dir,"exp.txt"), "w+") as outfile:
    outfile.write("\n".join(dates))

