from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import argparse
import time
import os

parser = argparse.ArgumentParser()

parser.add_argument("--ticker", "-t")

args = parser.parse_args()

ticker = args.ticker

timestamp = time.strftime("%m-%d-%Y_%H:%M")

cwd = os.getcwd()
exp_dir = "{}/exp.txt".format(ticker)
save_dir = "{t}/{q}/".format(t=ticker, q=timestamp)

if not os.path.exists(os.path.join(cwd, save_dir)):
    os.makedirs(os.path.join(cwd, save_dir))

chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the webdriver
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

    # Get the rows of the options table
    # rows = options_table.find_elements(By.TAG_NAME, "tr")
    # print(options_table.text)
    with open(os.path.join(cwd, save_dir, "{}.txt".format(d)), 'w+', newline='') as f:
        f.write(options_table.text)
    # Iterate through the rows and print the data
    # tot_data = []
    # for row in rows:
    #     cells = row.find_elements(By.TAG_NAME, "td")
    #     data = [cell.text for cell in cells]
    #     tot_data.append(data)
        
    # with open(os.path.join(cwd, save_dir, "{}.csv".format(d)), 'w+', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(tot_data)
    # print("written " + str(d))

# Close the webdriver
driver.close()