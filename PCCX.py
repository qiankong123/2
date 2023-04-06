import requests
from bs4 import BeautifulSoup

# Make a GET request to the website
response = requests.get('https://www.example.com')

# Parse the HTML content of the website using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the relevant data on the website using BeautifulSoup's find() or find_all() methods
data = soup.find('div', {'class': 'example-class'}).text

# Display the extracted data
print(data)