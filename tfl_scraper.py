from selenium import webdriver
import time
import re
import pandas as pd
import requests
from io import StringIO

# Initialize the WebDriver
driver = webdriver.Chrome('/Users/syber/downloads/chromedriver-mac-arm64/chromedriver')  # Replace with your WebDriver's path

# Open the webpage
driver.get('https://cycling.data.tfl.gov.uk/')

# Wait for the dynamic content to load
time.sleep(10)  # Adjust this time based on the page's load time

# Locate the div with class 'container'
container_div = driver.find_element_by_class_name('container')

# Retrieve and print the HTML content of the div
div_content = container_div.get_attribute('innerHTML')

rows = container_div.find_elements_by_tag_name('tr')

# List to store the CSV file links
csv_file_links = []

pattern = r'\d{3}JourneyDataExtract\d{2}(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(202[0-3])-\d{2}(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(202[1-3])\.csv'

csv_file_links = []

# Assuming 'rows' is a list of elements representing the rows in a table
for row in rows:
    try:
        # Find the <a> element and get its href attribute
        link = row.find_element_by_tag_name('a')
        url = link.get_attribute('href')

        # Check if the URL matches the naming convention
        if re.search(pattern, url):
            # Add the URL to the list
            csv_file_links.append(url)
    except Exception as e:
        # Handle the case where no link is found in the row
        print(f"An error occurred: {e}")

# Assuming 'driver' is your WebDriver instance
driver.quit()

# Print the list of CSV file links
for link in csv_file_links:
    print(link)

dataframes = []
df_count = 0

for url in csv_file_links:
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Read the content of the file into a DataFrame
            df = pd.read_csv(StringIO(response.content.decode('utf-8')), low_memory=False)
            # Append the DataFrame to the list
            df_count += 1
            print(f'df{df_count} has been processed, URL: {url}')
            dataframes.append(df)
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

combined_df = pd.concat(dataframes, ignore_index=True)

print(combined_df.head())
print(combined_df.shape) 

checkah = input("Hit 1 to proceed and save the CSV if you are happy:")

if checkah == "1":
    combined_df.to_csv('cycling.csv', index=False)