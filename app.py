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
    session = Session(engine)
    results = session.query(Quotes.quote).all()
    return jsonify(quotes=quotes)

    session.close()


# list author name
@app.route("/authors")
def authors():
    session = Session(engine)
    results = session.query(Quotes.author).all()
    return jsonify(authors=authors)


    session.close()


@app.route("/authors/< author name >")
def author_name():
    session = Session(engine)
# author info?
    session.close()

# list tags
@app.route("/tags")
def tags():
    session = Session(engine)
    results = session.query(Quotes.tags).all()
    return jsonify(tags=tags)

    session.close()



@app.route("/tags/< tag >")
def index():
    session = Session(engine)

    session.close()



@app.route("/top10tags")
def top_tags():
    session = Session(engine)
# list top 10 tags

    session.close()



if __name__ == "__main__":
    app.run(debug=True)