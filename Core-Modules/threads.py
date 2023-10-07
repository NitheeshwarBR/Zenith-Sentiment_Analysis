from selenium import webdriver
# import time 
from selenium.webdriver.common.by import By
# from datetime import datetime
from selenium.webdriver.chrome.options import Options
# import requests
# from datetime import datetime
# import logging
# import os
# import uuid
# from dotenv import load_dotenv
# import regex as re
# from datetime import datetime
# import csv

async def Comments(link,envir):
    if envir=="uat":
        # CALLBACK_URL = os.environ.get("CALLBACKURL")
        # print(CALLBACK_URL)
        # time.sleep(5)
        # logging.basicConfig(level=logging.INFO,filename="log.log",filemode="w",format="%(asctime)s  -  %(levelname)s   -   %(message)s")

        # website ="https://www.amazon.in/Motorola-Aurora-Green-128GB-Storage/dp/B0CGJBFWN3/ref=sr_1_3?crid=CF0RKQE51DB0&keywords=mobiles&qid=1694369926&sprefix=mobile%2Caps%2C211&sr=8-3"
        # website="https://www.threads.net/@ishansharma7390/post/CwDhaXevirT"
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # Create WebDriver instance with ChromeOptions
        driver = webdriver.Chrome(options=chrome_options)     
        driver.get(link)
        #sleep after loading website 
        # time.sleep(5)
        # logging.info("website loaded")
        # userNames=[]
        # userElement = driver.find_elements(By.CSS_SELECTOR,'.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xp07o12.xzmqwrg.x1citr7e.x1kdxza.xt0b8zv')
        # print(element)
        # for i in userElement:
        #     title =i.text
        #     userNames.append(title)
        #     # print("title:",title)
        # # print(userNames[:5])
        commentElement=[]
        element = driver.find_elements(By.CSS_SELECTOR,'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xjohtrz.xo1l8bm.xp07o12.xat24cr.xdj266r')
        # print(element)
        for i in element:
            title =i.text
            commentElement.append(title)
            # print("title:",title)
        # print(commentElement[:5])
        # csv_file_path="my_data.csv"
        # with open(csv_file_path, mode='w', newline='',encoding="utf-8") as csv_file:
        # # Create a CSV writer
        #     csv_writer = csv.writer(csv_file)

        #     # Write the header row
        #     csv_writer.writerow(['UserName','Summary'])  # Replace with your column headers

        #     # Use zip to iterate through the lists simultaneously and write them as rows
        #     for data_row in zip(userNames,commentElement):
        #         csv_writer.writerow(data_row)
        return commentElement
# Comments("https://www.threads.net/@ishansharma7390/post/CwDhaXevirT","uat")