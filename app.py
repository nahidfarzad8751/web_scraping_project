import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/quotes.sqlite")

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

app = Flask(__name__)

# create the routes

@app.route("/")
def index():
       """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/quotes<br/>"
        f"api/v1.0/authors<br/>"
        f"/api/v1.0/authors/< author name<br/>"
        f"/api/v1.0/tags><br/>"
        f"/api/v1.0/tags/< tag><br/>"
        f"/api/v1.0/top10tags<br/>"
    )


@app.route("/quotes")
def quotes():

 # total # scraped
 # quotes: 
 #      text:
 #      author name
 #      tags   
    session = Session(engine)
    results = session.query(Quotes.quote).count()
    return jsonify(quotes=quotes)

    session.close()


@app.route("/authors")
def authors():
#total # scraped
# details:
    # name:
    # description
    # born
    # count: total # of quotes by this author
    # quotes:
        # text
        # tags
    session = Session(engine)
    results = session.query(Quotes.author).all()
    return jsonify(authors=authors)


    session.close()


@app.route("/authors/< author name >")
def author_name():
#name
#description
#born
# # of quotes
# quotes:
    # text:
    # tags:
    session = Session(engine)

    session.close()


@app.route("/tags")
def tags():
# count
# details:
    # name
    # # of quotes
    # quotes:
        #text: 
        # tags:
    session = Session(engine)
    results = session.query(Quotes.tags).all()
    return jsonify(tags=tags)

    session.close()



@app.route("/tags/< tag >")
def index():
    # tag:
    # count: # of quotes this tag appears in
    # quote:
        #quote
        # tags
    session = Session(engine)

    session.close()



@app.route("/top10tags")
def top_tags():
# tag
# quote count
    session = Session(engine)

    session.close()



if __name__ == "__main__":
    app.run(debug=True)