#dependencies
import pandas as pd
import requests
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template, redirect

executable_path = {'executable_path': 'chromedriver'}

app=Flask(__name__)
client=pymongo.MongoClient('mongodb://localhost:27017')
db=client.mars
collection = db.mars
client.drop_database("mars")
db.collection.insert([
    {
        "a":"2",
        "b":"4"
    },
    {
        "c":"6",
        "d":"8"
    }
])

@app.route("/")
def index():
    mars=list(db.collection.find())
    print("THIS IS A TEST OF THE PRINT FUNCTION")
    return render_template("index.html")

#@app.route("/scrape")

if __name__ == "__main__":
    app.run(debug=True)

#Part 1: NASA MARS NEWS
browser = Browser('chrome', **executable_path, headless=False)
browser.visit("https://mars.nasa.gov/news")
soup = bs(browser.html,'html.parser')
news_title=soup.find(class_="content_title").text
news_paragraph=soup.find(class_="article_teaser_body").text
print(news_title,"\n\n",news_paragraph)

#Part 2: JPL SPACE IMAGES- FEATURED IMAGE
browser = Browser('chrome', **executable_path, headless=False)
browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
soup = bs(browser.html,'html.parser')
pic=soup.find("article",class_="carousel_item")
p = pic.find("a")
#we have the small/medium image, with a link to the
#page that contains the full version.
browser.visit("https://www.jpl.nasa.gov" + p["data-link"])
soup = bs(browser.html,"html.parser")
pic=soup.find("img", class_="main_image")
pic_url = "https://www.jpl.nasa.gov" + pic["src"]
print(pic_url)
#this is the full hi-res version of the picture found in 1st URL

#Part 3: MARS WEATHER
browser = Browser('chrome', **executable_path, headless=False)
browser.visit("https://twitter.com/marswxreport")
soup = bs(browser.html,"html.parser")
mars_weather = soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)

#Part 4: MARS FACTS
browser = Browser('chrome', **executable_path, headless=False)
browser.visit("https://space-facts.com/mars/")
soup = bs(browser.html,"html.parser")
table = soup.find("table",id="tablepress-mars")
labels = table.find_all("td",class_="column-1")
data = table.find_all("td",class_="column-2")
data_list = []
for l in labels:
    data_list.append([l.text, data[labels.index(l)].text])
data_df = pd.DataFrame(data_list,columns=["Category","Data"])
data_html_string = data_df.to_html().replace("\n","").replace("\\n","")
print(data_html_string)

#Part 5: MARS HEMISPHERES
browser = Browser('chrome', **executable_path, headless=False)
browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
soup = bs(browser.html,"html.parser")
images = soup.find_all("a",class_="itemLink product-item")
link_list = []
for i in images:
    link_list.append(i["href"])
    links=(list(set(link_list)))
img_dict={}
img_url_list=[]
for link in links:
    browser.visit("https://astrogeology.usgs.gov" + link)
    soup=bs(browser.html,"html.parser")
    imgurl = soup.find(class_="downloads").find("a")["href"]
    imgtitle = soup.find("h2").text
    img_dict=({"title":imgtitle,"img_url":imgurl})
    img_url_list.append(img_dict)
print(img_url_list)