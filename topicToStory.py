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

# story for "normal" aspect ratio
def createStory1(img, title, desc, url):
    newSize = (1920, 1080)
    img = img.resize(newSize)
    croppedImg = img.crop((640, 0, 1280, 1080))

    imgWidth = croppedImg.width
    imgHeight = croppedImg.height

    robotoBold = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Bold.ttf', math.ceil(imgWidth / imgHeight) * 25)
    robotoNorm = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Black.ttf', math.ceil(imgWidth / imgHeight) * 25)

    draw = ImageDraw.Draw(croppedImg)

    # design idea for TAMU branding purposes
    draw.rectangle((0, 0, 35, 360), fill=(0,60,113))
    draw.rectangle((0, 360, 35, 720), fill=(91,98,54))
    draw.rectangle((0, 720, 35, 1080), fill=(116,79,40))

    # article title background
    draw.rectangle((60, 60, 610, 120), fill="black")
    # article title
    draw.rectangle((50, 50, 600, 110), fill="white")

    draw.text((60, 50), "\n".join(textwrap.wrap(title,  width=45)), fill='black', font=robotoBold)
    
    # width = arialFont.getsize(t)[0]

    # print(width)

    # article desc background
    draw.rectangle((210, 450, 600, 650), fill="black")
    # article desc
    draw.rectangle((200, 440, 590, 640), fill="white")

    draw.text((210, 440), "\n".join(textwrap.wrap(desc,  width=30)), fill='black', font=robotoNorm)

    # article url background
    draw.rectangle((60, 1010, 610, 1070), fill="black")
    # article url
    draw.rectangle((50, 1000, 600, 1060), fill="white")

    draw.text((60, 1000), "\n".join(textwrap.wrap(url, width=45)), fill='black', font=robotoNorm)

    return croppedImg

# story for "not normal" aspect ratio
def creatStory2():
    backgroundImg = Image.open('background.png')
    newSize = (1920, 1080)
    backgroundImg = backgroundImg.resize(newSize)
    newImg = backgroundImg.crop((640, 0, 1280, 1080))
    return newImg

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

    # original image
    img = Image.open(BytesIO(response.content))


    # print("img height " + str(img.height))
    # print("img width " + str(img.width))

    # imgHeight = img.height
    # imgWidth = img.width

    # # fontsFolder = 'FONT_FOLDER'
    # robotoBold = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Bold.ttf', math.ceil(imgWidth / imgHeight) * 25)
    # robotoNorm = ImageFont.truetype(r'C:\CSCE445\Story2Instagram\static\fonts\Roboto-Black.ttf', math.ceil(imgWidth / imgHeight) * 25)
    # im = Image.open('background.png')

    storyImg = createStory1(img, t, d, url)
    storyImg2 = creatStory2()


    # draw.rectangle((40, 1400, 1400, 400), fill="white")
    # im.paste(img, (60,600))

    # frontA, backA = split(d)

    # print(d)
    # print(frontA)
    # print(backA)

    # draw.rectangle((40, 1900, 1400, 1500), fill="white")

    # # draw.text((0, 1600), backCaption, fill='black', font=arialFontsM)

    # GAR -> Good Aspect Ratio
    # BAR -> Bad Aspect Ratio

    new_name = "topic2instagramGAR_" + str(time.time()) + ".png"
    new_name2 = "topic2instagramBAR_" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagramGAR_'):  # not to remove other images
            os.remove('static/' + filename)
        if filename.startswith('toptic2instramBAR_'):
            os.remove('static/' + filename)

    storyImg.save('static/' + new_name)
    storyImg2.save('static/' + new_name2)
    return new_name, new_name2