from flask import Flask, render_template, request, redirect, url_for
from topicToStory import *
import time
import os
import urllib2 as urllib
app = Flask(__name__)

@app.route('/', methods=['post', 'get'])
def index():
        message = ''
        if request.method == 'POST':
                topic = request.form.get('topic')  # access the data inside 

                if topic is not "":
                        return redirect(topic)
                        # render_template(f"/{username}")
                else:
                        message = "No Topic Input"
        return render_template("index.html", message=message)


@app.route('/<name>',  methods=['post', 'get'])
def choose_article(name):
        if request.method == 'POST':
                topic = request.form.get('topic')  # access the data inside
                return redirect(topic)
                # render_template(f"/{username}")
        newsapi = NewsApiClient(api_key='be667b6da1734020a35b7c340f255a28')
        all_articles = newsapi.get_everything(q=name)
        return render_template("articles.html", topic=name, articles=all_articles['articles'])

@app.route('/picture')
def show_picture():
        name = request.args.get('topic',None)
        indexx = request.args.get('id',type=int)
        back = request.args.get('back',type=str) # file name of background image in static/backgrounds
        img_name = createImage(name, indexx, back)
        time.sleep(.5)
        return render_template("picture.html", picture=img_name)

@app.route('/background')
def choose_background():
        name = request.args.get('topic',None)
        indexx = request.args.get('id',type=int)
        picid = request.args.get('picart',type=str)
        # save picid to static/backgrounds
        fd = urllib.urlopen(picid)
        imgFile = BytesIO(fd.read())
        p = Image.open(imgFile)
        p = p.save("static/backgrounds/articlepic.png")
        pics = os.listdir('static/backgrounds/')
        return render_template("background.html", backgrounds=pics, topic=name, id=indexx, picart=picid)


if __name__ == '__main__':
        app.run()