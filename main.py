import os
from requests_html import HTMLSession
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
 
account_sid = os.environ['TWILIO_SID'] 
auth_token = os.environ['TWILIO_TOKEN']
client = Client(account_sid, auth_token)

os.environ['MOZ_HEADLESS'] = '1'
driver = webdriver.Firefox()

global pho
layout = [
[sg.Text('Enter Product Link')], [sg.InputText(size =(15, 1), key="OUTPUT")],
[sg.Text('Enter your phone number (Only numbers)')], [sg.InputText(size =(15, 1), key="PHONE")],
[sg.Submit()]
]
window = sg.Window('Link Entry Window', layout)
event, value = window.read()
if event =="Submit":
    val = value["OUTPUT"]
    pho = value["PHONE"]
window.close()

pho.replace(" ","")
driver.get(val)
try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, "comparison_add_to_cart_button2-announce"))
    )
finally:
    message = client.messages.create(   
        body='Your item is back in stock!',  
        from_='+13524969164',  
        to='+1'+pho
    ) 
    print(message.sid)
    driver.quit()

