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
url = 'https://www.copart.ca/lotSearchResults?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22TITL%22:%5B%22title_group_code:TITLEGROUP_C%22%5D,%22MAKE%22:%5B%22lot_make_desc:%5C%22HONDA%5C%22%22%5D,%22VEHT%22:%5B%22vehicle_type_code:VEHTYPE_V%22,%22veh_cat_code:VEHCAT_S%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'

# Create a folder to save images
folder_name = 'car_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize WebDriver and open the page
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
image_tags = soup.find_all('img', alt='Lot Image')

# Loop through the image tags and download each image
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for idx, img_tag in enumerate(image_tags):
    # Get the 'src' attribute (image URL)
    img_url = img_tag.get('src')
    
    # Resolve relative URLs
    img_url = urljoin(url, img_url)

    # Check if the URL starts with http/https
    if img_url.startswith('http'):
        # Try to download the image
        try:
            img_data = requests.get(img_url, headers=headers).content
            img_name = f"image_{idx + 1}.jpg"
            
            # Save the image in the folder
            img_path = os.path.join(folder_name, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded {img_name} from {img_url}")
        
        except Exception as e:
            print(f"Failed to download image {idx + 1}: {e}")
        
        # Add delay to avoid getting blocked
        time.sleep(2)
    else:
        print(f"Skipping invalid image URL: {img_url}")

print("Image download complete!")
