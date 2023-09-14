from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import requests
from datetime import datetime
import logging
import os
import uuid
from dotenv import load_dotenv
import regex as re
from datetime import datetime
import csv

def facebookComments(envir):
    if envir=="uat":
        CALLBACK_URL = os.environ.get("CALLBACKURL")

        logging.basicConfig(level=logging.INFO,filename="log.log",filemode="w",format="%(asctime)s  -  %(levelname)s   -   %(message)s")

       
        website="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2FDishaPatani%2Fposts%2Fpfbid02FXLWEEbwTQ4XgKahETpyS9hDFHdwXziUdBwEee7R1WmCioCbjLV9JXwvUpZWL7Anl&show_text=true&width=500"
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # Create WebDriver instance with ChromeOptions
        driver = webdriver.Chrome(options=chrome_options)     
        driver.get(website)
        #sleep after loading website 
        time.sleep(5)

        #click on comments
        element = driver.find_element(By.CLASS_NAME,'_29bd')
        href_value = element.get_attribute('href')
        driver.get(href_value)
        time.sleep(5)
        
        userList=[]
        Comment_list=[]
        comments= driver.find_elements(By.CLASS_NAME,'x1y1aw1k')


        for element in comments :

            # print("\ntext:",element.text,":")
            text = str(element.text.strip())
            pattern= r"Top fan"
            match = re.search(pattern,text)
            modified_string=str()
            if match:
                end_index = match.end()
                
         
                modified_string =text[end_index:]
                lines=modified_string.strip().splitlines()
        
                if(len(lines)<2):
                    continue
                Comment_list.append("".join(lines[1:]))
                userList.append(lines[0])

            else:
                lines=text.strip().splitlines()

                if(len(lines)<2):
                    continue
                Comment_list.append("".join(lines[1:]))
                userList.append(lines[0])

facebookComments("uat")