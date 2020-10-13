from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import requests
from io import BytesIO
import os
import time
import sys


def split(s):
    half, rem = divmod(len(s), 2)
    return s[:half + rem], s[half + rem:]

def createImage(topic, loc):
    sys.tracebacklimit = 0
    location = loc - 1

    newsapi = NewsApiClient(api_key='be667b6da1734020a35b7c340f255a28')
    # articleTopic = input('Enter Topic:')
    all_articles = newsapi.get_everything(q=topic)

    # print(all_articles['articles'])

    # return loc

    u = all_articles['articles'][location]['urlToImage']
    t = all_articles['articles'][location]['title']
    d = all_articles['articles'][location]['description']
    url = all_articles['articles'][location]['url']

    response = requests.get(u)
    img = Image.open(BytesIO(response.content))

    im = Image.open('background.png')
    im.paste(img, (100,600))
    draw = ImageDraw.Draw(im)
    fontsFolder = 'FONT_FOLDER'
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 60)
    arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    draw.text((100, im.height/6), t, fill='white', font=arialFont)
    frontA, backA = split(d)
    draw.text((0, 1500), frontA, fill='white', font=arialFontsM)
    draw.text((0, 1600), backA, fill='white', font=arialFontsM)
    draw.text((0, 2200), url, fill='white', font=arialFontsM)

    new_name = "topic2instagram" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram_'):  # not to remove other images
            os.remove('static/' + filename)

    im.save('static/'+ new_name)
    return new_name