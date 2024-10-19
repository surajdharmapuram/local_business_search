# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep

_PREFIX =  "/Users/surajdharmapuram/Desktop/data"

def get_linked_subpage_urls(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and (path.startswith("/") or path.startswith(url)):
            path = urljoin(url, path)
            yield path

def download_url(url):
     return requests.get(url).text

def crawl(url):
    html = download_url(url)
    # TODO: also get the text of the main page.
    counter = 1
    for sub_url in get_linked_subpage_urls(url, html):
        # get the subpages.
        response = requests.get(sub_url)
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        p_data = [data.text for data in soup.find_all("p")]
        p_data.insert(0, sub_url)
        prefix = f"{_PREFIX}/{counter}"
        print(prefix)
        with open(f"{prefix}.txt", "w") as f:
            f.writelines([line + "\n" for line in p_data])
        counter += 1
        sleep(3)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://www.makernexus.org/'
    print(list(get_linked_subpage_urls(url, requests.get(url).text)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
