import os
import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lh_tool.Iterator import MultiProcess


class Spider:
    @staticmethod
    def crawl(url):
        response = urlopen(url)
        return response.read().decode()

    @staticmethod
    def parse(html, pattern):
        soup = BeautifulSoup(html, 'lxml')
        urls = soup.find_all('a', {'href': re.compile(pattern)})
        urls = list(set([url['href'] for url in urls]))
        return urls

    @staticmethod
    def download(url, filename):
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

    def run(self, url, pattern, save_path):
        html = self.crawl(url)
        urls = self.parse(html, pattern)
        filenames = [os.path.join(save_path, url.split('/')[-1]) for url in urls]
        MultiProcess(self.download).run(urls, filenames)


if __name__ == '__main__':
    url = 'https://www.cs.toronto.edu/~vmnih/data/mass_roads/test/map/index.html'
    pattern = '^http.*?.tif$'
    save_path = '../image/mass_roads/test'

    os.makedirs(save_path, exist_ok=True)

    Spider().run(url, pattern, save_path)
