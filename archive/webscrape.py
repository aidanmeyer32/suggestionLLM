# This script will scrape a website and save the contents to a new text file in the project folder. 

from bs4 import BeautifulSoup
import requests 

# Send a GET request to the FCC website and get the HTML content
html_text = requests.get("https://www.fcc.gov/about-fcc/what-we-do").text 

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_text, 'lxml')

# Find all headers (h1) and paragraphs (p) in the HTML
headers = soup.find_all('h1') 
paragraphs = soup.find_all('p')

# Print all headers
for header in headers: 
    title = header.text 
    print(title) 

# Print all paragraphs
for p in paragraphs:
    content = p.text
    print(content) 

# Write headers and paragraphs to a text file
with open("new.txt", "w") as file:
    for header in headers:
        file.write(header.text + "\n")
    for p in paragraphs:
        file.write(p.text + "\n")


