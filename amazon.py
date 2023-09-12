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

# Sample date text
date_texts = [
    "Reviewed in India on 23 August 2023",
    "Reviewed in India on 1 September 2023",
    "Reviewed in India on 17 July 2023",
    "Reviewed in India on 31 July 2023",
    "Reviewed in India on 29 June 2023",
]

# Define a mapping of month names to their numerical representations
month_mapping = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

# Function to convert date text to DD:MM:YYYY format
def convert_date_text(date_text):
    # Split the date text into words
    words = date_text.split()
    
    # Extract day, month, and year
    day = words[4]
    month = month_mapping[words[5]]
    year = words[6]
    
    # Format the date as DD:MM:YYYY
    formatted_date = f"{day}:{month}:{year}"
    
    return formatted_date

load_dotenv()


def productListing(envir):
    if envir=="uat":
        CALLBACK_URL = os.environ.get("CALLBACKURL")
        # print(CALLBACK_URL)
        # time.sleep(5)
        logging.basicConfig(level=logging.INFO,filename="log.log",filemode="w",format="%(asctime)s  -  %(levelname)s   -   %(message)s")

        # website ="https://www.amazon.in/Motorola-Aurora-Green-128GB-Storage/dp/B0CGJBFWN3/ref=sr_1_3?crid=CF0RKQE51DB0&keywords=mobiles&qid=1694369926&sprefix=mobile%2Caps%2C211&sr=8-3"
        website="https://www.amazon.in/Redmi-Storage-Powerful-Processor-Warranty/dp/B0C46KPXCM/ref=sr_1_5?crid=CF0RKQE51DB0&keywords=mobiles&qid=1694456523&sprefix=mobile%2Caps%2C211&sr=8-5&th=1"
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # Create WebDriver instance with ChromeOptions
        driver = webdriver.Chrome(options=chrome_options)     
        driver.get(website)
        #sleep after loading website 
        time.sleep(5)
        logging.info("website loaded")

        #getting the title 
        element = driver.find_element(By.XPATH,'//*[@id="productTitle"]')
        title =element.text
        print("title:",title)

        #getting the brand
        element1=driver.find_element(By.XPATH,'//*[@id="bylineInfo"]')
        brandName=element1.text
        print("brandName",brandName)

        #getting the overall rating
        overallRating=driver.find_element(By.XPATH,'//*[@id="acrPopover"]/span[1]/a/span')
        overallRating=overallRating.text
        print("overallRating",overallRating)

        #getting the number of ratings 
        numberOfRating=driver.find_element(By.XPATH,'//*[@id="acrCustomerReviewText"]')
        numberOfRating=numberOfRating.text.strip().split()[0]
        numberOfRating=int(numberOfRating.replace(",",""))
        
        print("numberOfRating",numberOfRating)

        #getting the price
        Price=driver.find_element(By.XPATH,'//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]')
        Price=Price.text
        print("Price",Price)

        #getting percentages 
        five_star_count = four_star_count = three_star_count = two_star_count = one_star_count = 0
        tags=driver.find_elements(By.CLASS_NAME,"a-link-normal")
        percentages=list()
        # print(tags)
        for tag in tags:
            try:
                # title=tag.get_attribute('title')
                textInside=tag.text
                pattern=r"^\d+%$"
                text=textInside.strip()
                # print(textInside)
                if(re.search(pattern,text)):
                    percentages.append(text)
                # print("try done")
            except:
                print("could not find title")
                continue
        print(percentages)
        i=0
        for percent in percentages:
                percentage = int(percent.strip('%'))
                if i==0:
                    five_star_count = (percentage / 100) * numberOfRating
                elif i==1:
                    four_star_count = (percentage / 100) * numberOfRating
                elif i==2:
                    three_star_count = (percentage / 100) * numberOfRating
                elif i==3:
                    two_star_count = (percentage / 100) * numberOfRating
                elif i==4:
                    one_star_count = (percentage / 100) * numberOfRating
                i+=1

        

        # Print the calculated counts
        print("Number of 5-star ratings:", int(five_star_count))
        print("Number of 4-star ratings:", int(four_star_count))
        print("Number of 3-star ratings:", int(three_star_count))
        print("Number of 2-star ratings:", int(two_star_count))
        print("Number of 1-star ratings:", int(one_star_count))

        #going to more reviews link 
        moreReviews=driver.find_element(By.XPATH,'//*[@id="reviews-medley-footer"]/div[2]/a')
        

        
        #product page url
        Product_page=driver.current_url
        moreReviews.click()
        time.sleep(5)

        #filter 5 star etc
        dropDownPage=driver.current_url
        dropDown=driver.find_element(By.XPATH,'//*[@id="a-autoid-5-announce"]')
        dropDown.click()

        dropDownElements=driver.find_element(By.ID,"star-count-dropdown_0")
    
        #click each element 
        dropDownElements.click()


        #counting the number of reviews
        textTag=driver.find_element(By.XPATH,'//*[@id="filter-info-section"]/div')
        textTag= textTag.text
        print("text",textTag)

        #extract the number 
        #Use regex to extract the value
        match = re.search(r'\d+ with reviews', textTag)
        value_with_reviews=int()
        if match:
            value_with_reviews = int(re.search(r'\d+', match.group()).group())
            print(value_with_reviews)
        else:
            print("Value not found in the text.")

        userList=list()
        while( not(driver.find_element(By.XPATH,'//*[@id="cm_cr-review_list"]/div[12]/div/a'))):
            #user name
            userNames=driver.find_elements(By.CLASS_NAME,"a-profile-name")
            for userName in userNames:
                userList.append(userName.text)

            print(userList)

            #user rating
            ratingsList=[]
            userRatings=driver.find_elements(By.XPATH,'//*[@class="a-section review aok-relative"]/div/div/div[2]/a/i/span')
            for i in userRatings:
                textTotal=i.get_attribute('outerHTML')
                # print(textTotal)
                textF=textTotal.split()[1]
                textF=textF[-3:]
                ratingsList.append(textF)
            print(ratingsList)


            #extracting summary 
            summary=[]
            summarys=driver.find_elements(By.XPATH,'//*[@class="a-section review aok-relative"]/div/div/div[2]/a/span[2]')
            # summarySpan=summary.get_attribute('outerHTML')
            for i in summarys:
                summary.append(i.text)

            print(summary)

            #extracting dates 
            datesByReview=[]
            dates=driver.find_elements(By.XPATH,'//*[@class="a-section review aok-relative"]/div/div/span')
            # summarySpan=summary.get_attribute('outerHTML')
            for i in dates:
                datesByReview.append(convert_date_text(i.text))
            print(datesByReview)


            #extract comments
            commentsByReview=[]
            comments=driver.find_elements(By.XPATH,'//*[@class="a-section review aok-relative"]/div/div/div[4]/span/span')
            # summarySpan=summary.get_attribute('outerHTML')
            for i in comments:
                commentsByReview.append(i.text)
            print(commentsByReview)
            


            #click on next page 
            nextButton=driver.find_element(By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
            nextButton.click()
            time.sleep(5)

            csv_file_path="my_data.csv"
            with open(csv_file_path, mode='w', newline='',encoding="utf-8") as csv_file:
            # Create a CSV writer
                csv_writer = csv.writer(csv_file)

                # Write the header row
                csv_writer.writerow(['UserName', 'Rating', 'Summary',"date","full Text"])  # Replace with your column headers

                # Use zip to iterate through the lists simultaneously and write them as rows
                for data_row in zip(userList,ratingsList,summary,datesByReview,commentsByReview):
                    csv_writer.writerow(data_row)
                
            # if(driver.find_elements(By.XPATH,'//*[@id="cm_cr-review_list"]/div[12]/div/a')):
            #     print("\nAbout to break ")
            #     time.sleep(10)
            #     driver.back()
            driver.get(dropDownPage)
            dropDown.click()













        
productListing("uat")