from flask import Flask, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import pymongo
from pymongo.mongo_client import MongoClient

application = Flask(__name__)
app= application

# MongoDB connection setup
uri = "mongodb+srv://sandeepkr:sandeepkr@cluster0.0niktmf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["test_web"]
collection = db["news"]

@app.route('/')
def home():
    ineuron_url = "https://www.nasa.gov/news/all-news/"
    uclient = urlopen(ineuron_url)
    page_html = uclient.read()
    uclient.close()
    page_soup = bs(page_html, "html.parser")

    articles = page_soup.find_all('div', class_='hds-content-item')
    news_data = []
    i=0
    for article in articles:
        i= i+1
        title = article.find('a', class_='hds-content-item-heading').text.strip()
        link = article.find('a')['href']
        news_data.append({'Id': i ,'title': title, 'link': link})

    df = pd.DataFrame(news_data)

    df.to_csv("csv_path.csv", index=False)

    # Insert data into MongoDB
    if news_data:
        collection.insert_many(news_data)
    
    return render_template('news.html', news_data=news_data)


if __name__ == '__main__':
    app.run(debug=True)
