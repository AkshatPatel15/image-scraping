import base64
import requests
from bs4 import BeautifulSoup
import os

# URL of the webpage to scrape images from
url = "https://turo.com/ca/en/search?country=CA&defaultZoomLevel=11&endDate=10%2F03%2F2024&endTime=10%3A00&isMapSearch=false&itemsPerPage=200&latitude=43.653226&location=Toronto%2C%20ON&locationType=CITY&longitude=-79.38318429999998&pickupType=ALL&placeId=GhIJ0ytlGeLQRUARZMxdS8jXU8A&region=ON&sortType=RELEVANCE&startDate=09%2F30%2F2024&startTime=10%3A00&useDefaultMaximumDistance=true"


response = requests.get(url)
webpage_content = response.content

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(webpage_content, 'html.parser')

# Find all img tags
img_tags = soup.find_all('img')

# Extract the src attribute from each img tag
img_srcs = [img.get('src') for img in img_tags]

# Print the src attributes
for src in img_srcs:
    print(src)

