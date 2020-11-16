from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import requests
from io import BytesIO
import os
import time
import sys
import textwrap
import math

def createStory1(img, title, desc, url):
    imgWidth = img.width
    imgHeight = img.height

    fontsFolder = 'FONT_FOLDER'
    # Windows
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'),  math.ceil(imgWidth / imgHeight) * 25)
    arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'),  math.ceil(imgWidth / imgHeight) * 25)
    # Mac
    # arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', math.ceil(imgWidth / imgHeight) * 25)
    # arialFontsM = ImageFont.truetype('/Library/Fonts/Arial.ttf', math.ceil(imgWidth / imgHeight) * 25)

    draw = ImageDraw.Draw(img)

    # design idea for TAMU branding purposes
    draw.rectangle((0, 0, 35, 360), fill=(0,60,113))
    draw.rectangle((0, 360, 35, 720), fill=(91,98,54))
    draw.rectangle((0, 720, 35, 1080), fill=(116,79,40))

    # article title background
    draw.rectangle((60, 60, 610, 120), fill="black")
    # article title
    draw.rectangle((50, 50, 600, 110), fill="white")
    # title text
    draw.text((60, 50), "\n".join(textwrap.wrap(title,  width=45)), fill='black', font=arialFont)
            
    # article desc background
    draw.rectangle((210, 450, 600, 650), fill="black")
    # article desc
    draw.rectangle((200, 440, 590, 640), fill="white")
    # desc text
    draw.text((210, 440), "\n".join(textwrap.wrap(desc,  width=30)), fill='black', font=arialFontsM)

    # article url background
    draw.rectangle((60, 1010, 610, 1070), fill="black")
    # article url
    draw.rectangle((50, 1000, 600, 1060), fill="white")
    # url text
    draw.text((60, 1000), "\n".join(textwrap.wrap(url, width=45)), fill='black', font=arialFontsM)

    return img

def createStory2(im, artIm, t, d, url):
    im.paste(artIm, (100,625))
    draw = ImageDraw.Draw(im)
    # backgroundImg = ImageDraw.resize(newSize)
    fontsFolder = 'FONT_FOLDER'
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 60)
    # arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 60)
    arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    # arialFontsM = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
    draw.text((100, im.height/6), "\n".join(textwrap.wrap(t, width=45)), fill='white', font=arialFont)

    # draw.text((100, 1500), "\n".join(textwrap.wrap(frontA, width=45)), fill='white', font=arialFontsM)
    # draw.text((100, 1600), "\n".join(textwrap.wrap(backA, width=45)), fill='white', font=arialFontsM)
    draw.multiline_text((100, 1500), "\n".join(textwrap.wrap(d, width=50)), fill='white', spacing=15,font=arialFontsM)
    draw.text((100, 2200), "\n".join(textwrap.wrap(url, width=50)), fill='white', font=arialFontsM)

    return im

def createImage(topic, loc, backgroundPath):
    sys.tracebacklimit = 0
    location = loc - 1

    newsapi = NewsApiClient(api_key='87f90668eabb44b98fa88a4f007804b5')
    # articleTopic = input('Enter Topic:')
    all_articles = newsapi.get_everything(q=topic)

    # potentially play around w/ img resize to get uniform dimensions

    u = all_articles['articles'][location]['urlToImage']
    t = all_articles['articles'][location]['title']
    d = all_articles['articles'][location]['description']
    url = all_articles['articles'][location]['url']


    response = requests.get(u)
    
    img = Image.open(BytesIO(response.content)) # article image

    im = Image.open('static/backgrounds/' + backgroundPath) # background image

    storyImg = im

    if(backgroundPath == "articlepic.png"):
        storyImg = createStory1(im, t, d, url)
    else:
        storyImg = createStory2(im, img, t, d, url)

    new_name = "topic2instagram" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram'):  # not to remove other images
            os.remove('static/' + filename)

    storyImg.save('static/' + new_name)
    
    return new_name