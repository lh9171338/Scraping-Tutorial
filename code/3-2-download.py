import os
import requests
from urllib.request import urlretrieve

save_path = '../image'
os.makedirs(save_path, exist_ok=True)

IMAGE_URL = "https://mofanpy.com/static/img/description/learning_step_flowchart.png"


def urllib_download():
    urlretrieve(IMAGE_URL, os.path.join(save_path, 'image1.png'))      # whole document


def request_download():

    r = requests.get(IMAGE_URL)
    with open(os.path.join(save_path, 'image2.png'), 'wb') as f:
        f.write(r.content)                      # whole document


def chunk_download():
    import requests
    r = requests.get(IMAGE_URL, stream=True)    # stream loading

    with open(os.path.join(save_path, 'image3.png'), 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)


urllib_download()
print('download image1')
request_download()
print('download image2')
chunk_download()
print('download image3')

