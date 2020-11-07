from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import requests
from io import BytesIO
import os
import time
import sys
import textwrap
import math

def split(s):
    half, rem = divmod(len(s), 2)
    return s[:half + rem], s[half + rem:]

def createStory1(img, title, desc, url):
    imgWidth = img.width
    imgHeight = img.height

    # robotoBold = ImageFont.truetype('/Library/Fonts/Arial.ttf', int(math.ceil(imgWidth / imgHeight) * 25))
    # robotoNorm = ImageFont.truetype('/Library/Fonts/Arial.ttf', int(math.ceil(imgWidth / imgHeight) * 25))
    arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 60)
    arialFontsM = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)

    draw = ImageDraw.Draw(img)

    # design idea for TAMU branding purposes
    # draw.rectangle((0, 0, 35, 360), fill=(0,60,113))
    # draw.rectangle((0, 360, 35, 720), fill=(91,98,54))
    # draw.rectangle((0, 720, 35, 1080), fill=(116,79,40))

    # article title background
    draw.rectangle((95, img.height/6, 1360, img.height/6+160), fill="black")
    # article title
    draw.rectangle((85, img.height/6-10, 1350, img.height/6+150), fill=(255,255,255,128))
    
    # draw.text((60, 50), "\n".join(textwrap.wrap(title,  width=45)), fill='black', font=robotoBold)
    draw.text((100, img.height/6), "\n".join(textwrap.wrap(title, width=48)), fill='black', font=arialFont)
    
    # article desc background
    draw.rectangle((195, 1250, 1260, 1760), fill="black")
    # article desc
    draw.rectangle((185, 1240, 1250, 1750), fill="white")

    draw.multiline_text((200, 1250), "\n".join(textwrap.wrap(desc,  width=45)), fill='black', spacing=10, font=arialFontsM)

    # article url background
    draw.rectangle((95, 2200, 1360, 2350), fill="black")
    # article url
    draw.rectangle((85, 2190, 1350, 2340), fill="white")

    draw.text((100, 2200), "\n".join(textwrap.wrap(url, width=48)), fill='black', font=arialFontsM)

    return img

def createStory2(im, artIm, t, d, url):
    im.paste(artIm, (100,625))
    draw = ImageDraw.Draw(im)
    fontsFolder = 'FONT_FOLDER'
    # arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 60)
    arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 60)
    # arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    arialFontsM = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
    draw.text((100, im.height/6), "\n".join(textwrap.wrap(t, width=45)), fill='white', font=arialFont)
    frontA, backA = split(d)
    # draw.text((100, 1500), "\n".join(textwrap.wrap(frontA, width=45)), fill='white', font=arialFontsM)
    # draw.text((100, 1600), "\n".join(textwrap.wrap(backA, width=45)), fill='white', font=arialFontsM)
    draw.multiline_text((100, 1500), "\n".join(textwrap.wrap(d, width=50)), fill='white', spacing=15,font=arialFontsM)
    draw.text((100, 2200), "\n".join(textwrap.wrap(url, width=50)), fill='white', font=arialFontsM)

    return im

def createImage(topic, loc, backgroundPath):
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
    img = Image.open(BytesIO(response.content)) # article image

    im = Image.open('static/backgrounds/' + backgroundPath) # background image

    storyImg = im
    if(backgroundPath == "articlepic.png"):
        # newSize = (2720, 2960)
        # im = im.resize(newSize)
        # im = im.crop((640, 0, 2080, 2960))
        storyImg = createStory1(im, t, d, url)
    else:
        storyImg = createStory2(im, img, t, d, url)

    # old code beginning
    # im.paste(img, (100,600))
    # draw = ImageDraw.Draw(im)
    # fontsFolder = 'FONT_FOLDER'
    # # arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 60)
    # arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 60)
    # # arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    # arialFontsM = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
    # draw.text((100, im.height/6), t, fill='white', font=arialFont)
    # frontA, backA = split(d)
    # draw.text((0, 1500), frontA, fill='white', font=arialFontsM)
    # draw.text((0, 1600), backA, fill='white', font=arialFontsM)
    # draw.text((0, 2200), url, fill='white', font=arialFontsM)
    # old code ending

    new_name = "topic2instagram" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram'):  # not to remove other images
            os.remove('static/' + filename)

    im.save('static/'+ new_name)
    return new_name