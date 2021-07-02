
import requests
from bs4 import BeautifulSoup

# https://www.parsehub.com/blog/web-scraping-examples/#:~:text=Many%20real%20estate%20agents%20use,this%20information%20onto%20their%20website.
# https://www.directautomecca.com/view-inventory.aspx
# https://realpython.com/beautiful-soup-web-scraper-python/#part-2-scrape-html-content-from-a-page

URL = 'https://www.directautomecca.com/view-inventory.aspx'
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())


