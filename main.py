'''
This project consists of building a Python app that scrapes the stock price change percentage 
from this webpage: https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6 and sends an email 
if the stock price is below -0.10%
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import yagmail

def get_driver():
    # Set options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
    return driver

# Get the stock price
def get_stock_price(driver):
    stock_price = driver.find_element(by="xpath", value = "/html/body/div[1]/div/section[1]/div/div/div[2]/span[2]").text
    return float(stock_price[:-2])

# Send an email
def send_email(stock_price):
    sender = 'tony84@gmail.com'
    receiver = 'awill@jamsol.com'

    subject = "The stock price is below -0.10%"


    contents = f"The current stock price is: {stock_price}%"

    yag = yagmail.SMTP(user=sender, password=os.environ['GMPASS'])
    yag.send(to=receiver, subject=subject, contents=contents)
    print("Email Sent!")

driver = get_driver()
price_percentage = get_stock_price(driver)

if price_percentage < -0.10:
    print("Sending email")
    send_email(price_percentage)