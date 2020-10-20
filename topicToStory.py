from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import requests
from io import BytesIO
import os
import time
import sys
import textwrap
import math


# def split(s):
#     half, rem = divmod(len(s), 2)
#     return s[:half + rem], s[half + rem:]

def createImage(topic, loc):
    sys.tracebacklimit = 0
    location = loc - 1

    newsapi = NewsApiClient(api_key='87f90668eabb44b98fa88a4f007804b5')
    # articleTopic = input('Enter Topic:')
    all_articles = newsapi.get_everything(q=topic)

    # print(all_articles['articles'])

    # return loc

    # potentially play around w/ img resize to get uniform dimensions

    u = all_articles['articles'][location]['urlToImage']
    t = all_articles['articles'][location]['title']
    d = all_articles['articles'][location]['description']
    url = all_articles['articles'][location]['url']

    response = requests.get(u)
    img = Image.open(BytesIO(response.content))

    newSize = (1920, 1080)

    img = img.resize(newSize)

    print("img height " + str(img.height))
    print("img width " + str(img.width))

    imgHeight = img.height
    imgWidth = img.width

    print(math.ceil(imgWidth / imgHeight))

    # fontsFolder = 'FONT_FOLDER'
    arialFont = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Bold.ttf', math.ceil(imgWidth / imgHeight) * 25)
    arialFontsM = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Black.ttf', math.ceil(imgWidth / imgHeight) * 15)
    # im = Image.open('background.png')
    draw = ImageDraw.Draw(img)

    # draw.rectangle((40, 200, 1400, 40), fill="white")

    draw.text((50, 50), "\n".join(textwrap.wrap(t,  width=math.ceil(imgHeight / 2))), fill='white', font=arialFont)
    

    # draw.rectangle((40, 1400, 1400, 400), fill="white")
    # im.paste(img, (60,600))
    draw.text((50, imgHeight - 50), "\n".join(textwrap.wrap(url, width=math.ceil(imgHeight / 2))), fill='white', font=arialFontsM)

    # frontA, backA = split(d)

    print(d)
    # print(frontA)
    # print(backA)

    # draw.rectangle((40, 1900, 1400, 1500), fill="white")
    draw.text((50, (imgHeight / 2) - 50), "\n".join(textwrap.wrap(d,  width=40)), fill='white', font=arialFontsM)
    # # draw.text((0, 1600), backCaption, fill='black', font=arialFontsM)

    new_name = "topic2instagram_" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram_'):  # not to remove other images
            os.remove('static/' + filename)

    img.save('static/'+ new_name)
    return new_name