#import dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import marsScrape

#create Flask instance
app = Flask(__name__)

#set up connection to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app)


@app.route("/")
def index():
    marsScrape = mongo.db.marsScrape.find_one()
    return render_template("index.html", marsScrape=marsScrape)

@app.route("/scrape")
def mars_Scrape():
    marsScrape = mongo.db.marsScrape
    marsData = marsScrape.scrape()
    marsScrape.update({}, marsData, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)