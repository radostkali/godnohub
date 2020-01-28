from PIL import Image
import requests
from io import BytesIO
import base64
from bs4 import BeautifulSoup
import json


def get_average_color(url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content)).resize((1, 1))
    pixel = img.getpixel((0, 0))
    if isinstance(pixel, int):
        color = pixel if pixel <= 160 else 160
        return '#' + ('{:02x}'.format(color) * 3)
    color = list(pixel)
    change_c = [1 if c > 160 else 0 for c in color]
    if sum(change_c) >= 2:
        for i in range(3):
            if color[i] > 160:
                odd = color[i] - 160
                color = [c - odd if c >= odd else 0 for c in color]
    return '#{:02x}{:02x}{:02x}'.format(*color)


def imgur_upload(url=None, file=None, basewidth=300):
    TOKEN = 'Bearer 97451c2553a2f23b3e50f2f30dd4825fd2a4ef8d'
    imgur_url = 'https://api.imgur.com/3/image'
    try:
        if url:
            image = is_url_image(url)
        elif file:
            image = file
        else:
            return None
        image = Image.open(BytesIO(image))
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
        buff = BytesIO()
        try:
            image.save(buff, format="JPEG")
        except Exception:
            image.save(buff, format="PNG")
        encoded_img = base64.b64encode(buff.getvalue())
        r = requests.post(imgur_url, headers={'Authorization': TOKEN},
                          data={'image': encoded_img})
        img_id = json.loads(r.text)['data']['id']
        return 'https://i.imgur.com/%s.jpg' % img_id
    except Exception as e:
        print('Error while image uploading:')
        print(e)
        return None


def is_url_image(url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.get(url)
    if r.headers["content-type"] in image_formats:
        return r.content
    return None


def search_images(title, count=6, page=1):
    search = title + ' обложка'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    r = requests.get('https://www.google.com/search?tbm=isch&tbs=isz:m&q=%s' % search, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    page_size = 6
    if page == 1:
        start = 0
        end = count
    else:
        start = count + (page_size*(page-2))
        end = count + (page_size*(page-1))
    if start != end:
        results = [json.loads(img.text)['ou'] for img in soup.find_all('div', {'class': 'rg_meta'})][start:end]
    else:
        results = []
    return results
