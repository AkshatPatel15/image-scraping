import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

# Set up Chrome options and specify the path to ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless (without opening the browser)
chrome_driver_path = "/Users/akshatpatel/Downloads/chromedriver-mac-arm64/chromedriver"  # Update with your chromedriver path

# Initialize the ChromeDriver service
service = Service(chrome_driver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL of the website to scrape
url = 'https://www.nawabmotors.ca/cars?make=&model=&Minyear=&Maxyear='

# Create a folder to save images
folder_name = 'car_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize WebDriver and open the page
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

# Scroll and wait for new content to load
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new data to load
    time.sleep(3)
    
    # Calculate new scroll height and compare it with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break  # If the height hasn't changed, we've reached the end of the page
    last_height = new_height

# After scrolling is complete, parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser
driver.quit()

# Find all image elements (usually in 'img' tags)
image_tags = soup.find_all('img')

# Loop through the image tags and download each image
for idx, img_tag in enumerate(image_tags):
    # Get the 'src' attribute (image URL)
    img_url = img_tag.get('src')
    
    # Resolve relative URLs
    img_url = urljoin(url, img_url)

    # Check if the URL starts with http/https
    if img_url.startswith('http'):
        # Try to download the image
        try:
            img_data = requests.get(img_url).content
            img_name = f"image_{idx + 1}.jpg"
            
            # Save the image in the folder
            img_path = os.path.join(folder_name, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded {img_name} from {img_url}")
        
        except Exception as e:
            print(f"Failed to download image {idx + 1}: {e}")
    else:
        print(f"Skipping invalid image URL: {img_url}")

print("Image download complete!")
