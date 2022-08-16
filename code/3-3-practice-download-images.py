from bs4 import BeautifulSoup
import requests
import os


if __name__ == '__main__':
    URL = "http://www.dili360.com/"
    save_path = '../image/dili360'
    os.makedirs(save_path, exist_ok=True)

    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'lxml')
    img_blocks = soup.find_all('li', {'class': 'img-block'})
    for img_block in img_blocks:
        imgs = img_block.find_all('img')
        names = img_block.find_all('h4')
        url = img_block.find('img')['src']
        name = img_block.find('h4').text

        r = requests.get(url, stream=True)
        image_file = os.path.join(save_path, name + '.jpg')
        with open(image_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print(f'Saved {image_file}')
