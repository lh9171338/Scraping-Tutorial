import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
import re
import multiprocessing as mp

base_url = "https://mofanpy.com/"
restricted_crawl = False
seen = set()
unseen = {base_url}


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1').get_text().strip()
    url = soup.find('meta', {'property': "og:url"})['content']
    urls = soup.find_all('a', {"href": re.compile('^https://mofanpy.com.+?/$')})
    page_urls = set([url['href'] for url in urls])
    return title, page_urls, url


async def crawl(url, session):
    r = await session.get(url)
    html = await r.text()
    return html


async def main(loop):
    pool = mp.Pool(2)               # slightly affected
    async with aiohttp.ClientSession() as session:
        count = 1
        while len(unseen) != 0:
            if restricted_crawl and len(seen) > 20:
                break
            tasks = [loop.create_task(crawl(url, session)) for url in unseen]
            finished, unfinished = await asyncio.wait(tasks)
            htmls = [f.result() for f in finished]

            parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
            results = [j.get() for j in parse_jobs]

            seen.update(unseen)
            unseen.clear()
            for title, page_urls, url in results:
                print(count, title, url)
                unseen.update(page_urls - seen)
                count += 1


if __name__ == "__main__":
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("Async total time: ", time.time() - t1)
