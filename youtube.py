import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time



def youtubeScraper(envir):
    if (envir=="uat"):
        # Replace 'your_youtube_link' with the URL of the YouTube video you want to scrape
        youtube_link = 'https://www.youtube.com/watch?v=B3jHItsUOcA'

        # Set the options for the Chrome WebDriver to open an incognito window
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        # Initialize the Selenium WebDriver for Chrome with incognito option
        driver = webdriver.Chrome(options=chrome_options)

        # Open the YouTube video page in the incognito tab
        driver.get(youtube_link)

        # Scroll down to load more comments (adjust the number of scrolls as needed)
        num_scrolls = 10
        for _ in range(num_scrolls):
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

        # Find the comment elements
        comments=list()
        userNames=list()
        comment_elements = driver.find_elements(By.ID, 'content-text')
        user_elements = driver.find_elements(By.ID, 'author-text')
        for i in user_elements:
            userNames.append(i.text)

        for j in comment_elements:
            comments.append(i.text)



        csv_file_path="my_data.csv"
        with open(csv_file_path, mode='w', newline='',encoding="utf-8") as csv_file:
        # Create a CSV writer
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(["UserName","comment"])  # Replace with your column headers

            # Use zip to iterate through the lists simultaneously and write them as rows
            for data_row in zip(userNames,comments):
                csv_writer.writerow(data_row)

        time.sleep(2)