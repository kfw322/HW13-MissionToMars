#dependencies
import json
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
import pandas as pd
import time

def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    mars = {}
    mars_data = {}

    """     #Part 1: NASA MARS NEWS
    browser.visit("https://mars.nasa.gov/news")
    soup = bs(browser.html,'html.parser')
    news_title=soup.find(class_="content_title").text
    news_paragraph=soup.find(class_="article_teaser_body").text
    #print(news_title,"\n\n",news_paragraph)
    mars["news_title"]=news_title
    mars["news_paragraph"]=news_paragraph

    #Part 2: JPL SPACE IMAGES- FEATURED IMAGE
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
    #print(pic_url)
    mars["featured_img_url"]=pic_url
    #this is the full hi-res version of the picture found in 1st URL

    #Part 3: MARS WEATHER
    browser.visit("https://twitter.com/marswxreport")
    soup = bs(browser.html,"html.parser")
    mars_weather = soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather)
    mars["mars_weather"]=mars_weather
    """

    #Part 4: MARS FACTS
    browser.visit("https://space-facts.com/mars/")
    soup = bs(browser.html,"html.parser")
    table = soup.find("table",id="tablepress-mars")
    labels = table.find_all("td",class_="column-1")
    data = table.find_all("td",class_="column-2")
    data_list = []
    for l in labels:
        data_list.append([l.text, data[labels.index(l)].text])
    data_df = pd.DataFrame(data_list,columns=["Category","Data"])
    data_html_string = data_df.to_html()#.replace("\n","").replace("\\n","")
    #data_html_string = str(" ".join(data_html_string.split()))
    #for th in range(0,9):
    #   data_html_string = data_html_string.replace(f"<th>{th}</th>","")
    #data_html_string = data_html_string.replace(r'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>Category</th> <th>Data</th> </tr> </thead> <tbody>',"<table>").replace(r'</tbody>',"")
    #print(data_html_string)
    mars["data_html_string"]=data_html_string 

    #Part 5: MARS HEMISPHERES
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    soup = bs(browser.html,"html.parser")
    images = soup.find_all("a",class_="itemLink product-item")
    link_list = []
    for i in images:
        link_list.append(i["href"])
        links=(list(set(link_list)))
    img_dict={}
    ic=1
    for link in links:
        browser.visit("https://astrogeology.usgs.gov" + link)
        soup=bs(browser.html,"html.parser")
        imgurl = soup.find(class_="downloads").find("a")["href"]
        imgtitle = soup.find("h2").text
        img_dict={"title":imgtitle,"img_url":imgurl}
        mars[str("hemisphere_url_dict_" + str(ic))]=img_dict
        ic+=1
    mars_data = mars
    print(mars_data)
    import win32api
    win32api.MessageBox(None,json.dumps(mars_data),"aaaaaaaaa")
    #mars_data = jsonify(news_title=news_title, news_paragraph=news_paragraph, featured_img_url=pic_url, mars_weather=mars_weather, data_html_string=data_html_string, hemisphere_url_list=img_url_dict)
    return mars_data