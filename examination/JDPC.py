# 5简单爬虫

# import requests
# from bs4 import BeautifulSoup
#
# # Define the URL to scrape
# url = 'https://www.example.com'
#
# # Send a GET request to the URL
# response = requests.get(url)
#
# # Parse the HTML content of the page using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Find all the links on the page
# links = soup.find_all('a')
#
# # Print out the href attribute of each link
# for link in links:
#     print(link.get('href'))


# # First, we need to import the necessary libraries
# import requests
# from bs4 import BeautifulSoup
# import os
#
# # Set the URL of the website you want to scrape
# url = "https://example.com"
#
# # Send a GET request to the URL
# response = requests.get(url)
#
# # Parse the HTML content of the page using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Find all the image tags on the page
# images = soup.find_all('img')
#
# # Create a directory to store the downloaded images
# if not os.path.exists('images'):
#     os.makedirs('images')
#
# # Loop through each image and download it
# for image in images:
#     # Get the source URL of the image
#     src = image['src']
#
#     # Send a GET request to the image URL
#     response = requests.get(src)
#
#     # Get the filename of the image
#     filename = os.path.join('images', src.split('/')[-1])
#
#     # Write the image content to a file
#     with open(filename, 'wb') as f:
#         f.write(response.content)



# Importing necessary libraries
import requests
from bs4 import BeautifulSoup

# URL of the webpage to be scraped
url = 'https://www.example.com'

# Sending a GET request to the URL
response = requests.get(url)

# Parsing the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Finding all the text on the page
text = soup.get_text()

# Printing the text
print(text)