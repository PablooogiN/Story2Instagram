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

@app.route('/<name>')
def choose_article(name):
        newsapi = NewsApiClient(api_key='87f90668eabb44b98fa88a4f007804b5')
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