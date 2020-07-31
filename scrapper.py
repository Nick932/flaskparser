from bs4 import BeautifulSoup
import requests

page_link ='https://vk.com'






def data_collector(page):
    page_response = requests.get(page, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    content = page_content.find_all()
    return content


def scrapper(page_link):
    #cpus = cpu_count()
    #workers = Pool(cpus)
    #results = workers.map(scrappy, page_link)
    results = data_collector(page_link)
    return results

if __name__ == '__main__':
    scrapper(page_link)







