from bs4 import BeautifulSoup
import requests

page_link ='https://vk.com'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
prices = page_content.find_all()


