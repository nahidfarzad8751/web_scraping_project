from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_craigslist

import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/quotes")
def quotes():



@app.route("/authors")
def authors():



@app.route("/authors/< author name >")
def author_name():


@app.route("/tags")
def tags():



@app.route("/tags/< tag >")
def index():



@app.route("/top10tags")
def top_tags():



if __name__ == "__main__":
    app.run(debug=True)