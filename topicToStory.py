from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import requests
from io import BytesIO
import os
import time
import sys
import textwrap


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

    fontsFolder = 'FONT_FOLDER'
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    arialFontsM = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 50)
    im = Image.open('background.png')
    draw = ImageDraw.Draw(im)

    draw.rectangle((40, 200, 1400, 40), fill="white")

    draw.text((50, 50), "\n".join(textwrap.wrap(t, width=50)), fill='black', font=arialFont)
    

    draw.rectangle((40, 1400, 1400, 400), fill="white")
    im.paste(img, (60,600))
    draw.text((100, 1275), "\n".join(textwrap.wrap(url, width=50)), fill='black', font=arialFontsM)

    # frontA, backA = split(d)

    print(d)
    # print(frontA)
    # print(backA)

    draw.rectangle((40, 1900, 1400, 1500), fill="white")
    draw.text((100, 1500), "\n".join(textwrap.wrap(d, width=50)), fill='black', font=arialFontsM)
    # # draw.text((0, 1600), backCaption, fill='black', font=arialFontsM)

    new_name = "topic2instagram_" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('topic2instagram_'):  # not to remove other images
            os.remove('static/' + filename)

    im.save('static/'+ new_name)
    return new_name