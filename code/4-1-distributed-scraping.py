from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import multiprocessing as mp
import re
import time


def crawl(url):
    response = urlopen(url)
    return response.read().decode()


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1').get_text().strip()
    url = soup.find('meta', {'property': "og:url"})['content']
    urls = soup.find_all('a', {"href": re.compile('^https://mofanpy.com.+?/$')})
    page_urls = set([url['href'] for url in urls])
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    page_urls2 = set([urljoin('https://mofanpy.com/', url['href']) for url in urls])   # remove duplication
    page_urls.update(page_urls2)
    return title, page_urls, url


if __name__ == '__main__':
    base_url = 'https://mofanpy.com/'
    restricted_crawl = False

    unseen = {base_url}
    seen = set()

    pool = mp.Pool(4)                       # number strongly affected
    count, t1 = 1, time.time()

    while len(unseen) != 0:                 # still get some url to visit
        if restricted_crawl and len(seen) > 20:
            break
        print('\nDistributed Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs]                                       # request connection
        htmls = [h for h in htmls if h is not None]     # remove None

        print('\nDistributed Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [j.get() for j in parse_jobs]                                     # parse html

        print('\nAnalysing...')
        seen.update(unseen)
        unseen.clear()

        for title, page_urls, url in results:
                print(count, title, url)
                count += 1
                unseen.update(page_urls - seen)

    print(f'Total time: {time.time()-t1:.1f}')
