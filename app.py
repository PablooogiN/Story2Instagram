from flask import Flask, render_template, request, redirect, url_for
from topicToStory import *
import time
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

# @app.route('/search', methods=['post', 'get'])
# def index():
#         message = ''
#         if request.method == 'POST':
#                 topic = request.form.get('topic')  # access the data inside
#                 return redirect(topic)
#                 # render_template(f"/{username}")
#         return render_template("articles.html")

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
        img_name = createImage(name, indexx)
        time.sleep(.5)
        return render_template("picture.html", picture=img_name)

if __name__ == '__main__':
        app.run()