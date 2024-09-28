import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL of the website to scrape
url = 'https://www.nawabmotors.ca/cars?make=&model=&Minyear=&Maxyear='

# Create a folder to save images
folder_name = 'car_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Send a GET request to fetch the webpage content
response = requests.get(url)
if response.status_code == 200:
    print("Successfully accessed the website!")
else:
    print("Failed to access the website.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Find all image elements (usually in 'img' tags)
image_tags = soup.find_all('img')

# Check if any images were found
if not image_tags:
    print("No images found on the page.")
    exit()

# Loop through the image tags and download each image
for idx, img_tag in enumerate(image_tags):
    # Get the 'src' attribute (image URL)
    img_url = img_tag.get('src')
    
    # Resolve relative URLs to absolute URLs
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
