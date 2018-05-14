from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import json
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/")
def index():
    
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)

@app.route("/scrape")
def scrape():
    mongo.db.drop_collection("mars")
    import win32api
    win32api.MessageBox(None,"sup","bbbbbb")
    mars = mongo.db.mars
    win32api.MessageBox(None,"hi","ccccccccc")
    mars_data = scrape_mars.scrape()
    print(mars_data)
    win32api.MessageBox(None,json.dumps(mars_data),"dddddddddd")
    mars.update({}, mars_data, upsert=True)
    win32api.MessageBox(None,"ayy lmao","eeeeeeeeeeee")
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    app.run(debug=True)