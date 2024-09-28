import base64
import requests
from bs4 import BeautifulSoup
import os

# URL of the webpage to scrape images from
url = "https://turo.com/ca/en/search?country=CA&defaultZoomLevel=11&endDate=10%2F03%2F2024&endTime=10%3A00&isMapSearch=false&itemsPerPage=200&latitude=43.653226&location=Toronto%2C%20ON&locationType=CITY&longitude=-79.38318429999998&pickupType=ALL&placeId=GhIJ0ytlGeLQRUARZMxdS8jXU8A&region=ON&sortType=RELEVANCE&startDate=09%2F30%2F2024&startTime=10%3A00&useDefaultMaximumDistance=true"

# Send a request to the webpage and get the HTML content
response = requests.get(url)
webpage_content = response.content

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(webpage_content, 'html.parser')

# Find all img tags
img_tags = soup.find_all('img')

# Create a folder to save the images
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Process each img tag
for index, img in enumerate(img_tags):
    src = img.get('src')
    
    if src and src.startswith('data:image'):  # Check if src is base64 encoded
        # Find the base64 part of the src
        base64_str = src.split(',')[1]

        # Decode the base64 string
        img_data = base64.b64decode(base64_str)

        # Determine the image format (png or jpeg)
        img_format = "png" if "png" in src else "jpg"
        
        # Save the image to a file
        img_filename = f"downloaded_images/image_{index}.{img_format}"
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
        
        print(f"Saved image {index} as {img_filename}")
