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
    img = img.crop((640, 0, 1280, 1080))

    print("img height " + str(img.height))
    print("img width " + str(img.width))

    imgHeight = img.height
    imgWidth = img.width

    # fontsFolder = 'FONT_FOLDER'
    arialFont = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Bold.ttf', math.ceil(imgWidth / imgHeight) * 25)
    arialFontsM = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Black.ttf', math.ceil(imgWidth / imgHeight) * 25)
    # im = Image.open('background.png')
    draw = ImageDraw.Draw(img)

    # design idea for TAMU branding purposes
    draw.rectangle((0, 0, 35, 360), fill=(0,60,113))
    draw.rectangle((0, 360, 35, 720), fill=(91,98,54))
    draw.rectangle((0, 720, 35, 1080), fill=(116,79,40))

    # article title background
    draw.rectangle((60, 60, 610, 120), fill="black")
    # article title
    draw.rectangle((50, 50, 600, 110), fill="white")

    draw.text((60, 50), "\n".join(textwrap.wrap(t,  width=45)), fill='black', font=arialFont)
    
    # width = arialFont.getsize(t)[0]

    # print(width)

    # article desc background
    draw.rectangle((210, 450, 600, 650), fill="black")
    # article desc
    draw.rectangle((200, 440, 590, 640), fill="white")

    draw.text((210, 440), "\n".join(textwrap.wrap(d,  width=30)), fill='black', font=arialFontsM)

    # article url background
    draw.rectangle((60, 1010, 610, 1070), fill="black")
    # article url
    draw.rectangle((50, 1000, 600, 1060), fill="white")

    draw.text((60, 1000), "\n".join(textwrap.wrap(url, width=45)), fill='black', font=arialFontsM)


    # draw.rectangle((40, 1400, 1400, 400), fill="white")
    # im.paste(img, (60,600))

    # frontA, backA = split(d)

    print(d)
    # print(frontA)
    # print(backA)

    # draw.rectangle((40, 1900, 1400, 1500), fill="white")

    # # draw.text((0, 1600), backCaption, fill='black', font=arialFontsM)

    new_name = "topic2instagram_" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram_'):  # not to remove other images
            os.remove('static/' + filename)

    img.save('static/'+ new_name)
    return new_name