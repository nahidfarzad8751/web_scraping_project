import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json
from flask import Flask, jsonify
import pdb
from collections import OrderedDict
import pprint

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")
#engine = create_engine(f'postgresql://postgres:postgres@localhost:5432/customer_db')
engine =create_engine('postgres://fvrxkvnewvtszf:abb0db95fb45783bc324dd7fc23d3cd412dcb26b173906376407a5d54fd773d4@ec2-52-22-238-188.compute-1.amazonaws.com:5432/d3krndmoauivhr')
#connection = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
author = Base.classes.author
quotes = Base.classes.quotes

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # JSON objects are unordered structures


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    print('IDKLOL')
    sel = [author.name]
    #results = session.query(author.name).all()
    # Dict with date as the key and prcp as the value
    
    results = session.query(*sel).all()
    stations = list(np.ravel(results))

    return jsonify(stations=stations)
    

#####################################################################################
# AUTHORS
#####################################################################################
@app.route("/authors")
@app.route("/authors/<author_name>")
def authors(author_name=None):
    result = OrderedDict()
    result_set = engine.execute('''SELECT * FROM author
    order by name''')#This literally just return the same table
    total_details = result_set.rowcount #Need to find unique
    details = []
    
    print(f'The keys/column-names to the queried table are {result_set.keys()}')
    for row in result_set:#Loop through each unique author's name
        print(f'{row}')
        detail = {}
        if '\'' in row.name:#IF a name contains a single quote in SQL, things break down and you need to add a second to have in recognized
            name = name.replace('\'','\'\'')
        else:
            name = row.name
        detail['name'] = name
        
        detail['description'] = row.description
        detail['born'] = row.born
        print(row)
        author_quote_count = engine.execute(f''' SELECT COUNT(*) FROM quotes WHERE author_name LIKE \'{name}\' ''')
        detail['count'] = author_quote_count.scalar()
        author_quotes_list = author_quotes_list = engine.execute(f''' SELECT text FROM quotes WHERE author_name LIKE \'{name}\' ''').fetchall()
        author_quotes_list = np.ravel(author_quotes_list).tolist()
        detail['quotes'] = author_quotes_list
        author_tags_list = engine.execute(f''' SELECT tag FROM quotes q inner join tags t on q.id=t.quote_id WHERE author_name LIKE \'{name}\' ''').fetchall()
        author_tags_list = np.ravel(author_tags_list).tolist()
        detail['tags'] = author_tags_list
        pprint.pprint(detail,indent=4, width = 40, compact=True)
        details.append(detail)
        
    result['total'] = total_details
    result['details'] = details
    print(json.dumps(result, indent=5, ensure_ascii=False))
    
    if author_name:
        for sub in result['details']:
            #pdb.set_trace()
            if sub['name'] == author_name:
                pdb.set_trace()
                res = sub
                print(json.dumps(sub, indent=5, ensure_ascii=False))
                #break
                return jsonify(sub=sub)
    else:
        return jsonify(result=result)





#####################################################################################
# TOP 10 TAGS
#####################################################################################
@app.route("/top10tags")
def top10tags(author_name=None):
    result = OrderedDict()
    unique_tags_query = engine.execute('''SELECT DISTINCT tag FROM tags''')
    unique_tag_count = unique_tags_query.rowcount #Find all unique tags

    top10tags_tags_query = engine.execute('''SELECT tag, COUNT(*)
                                            FROM tags
                                            GROUP BY tag
                                            ORDER BY count DESC
                                            FETCH FIRST 10 ROWS ONLY;''').fetchall()

    top10tags_tags_list = np.ravel(top10tags_tags_query).tolist()
    details = []
    #print(f'The keys/column-names to the queried table are {top10tags_tags_query.keys()}')
    details = []
    for tag, tag_count in top10tags_tags_query:
        print(f'/n The tag {tag} was used {tag_count} times in quotes \n')
        detail = {}
        detail['tag'] = tag
        detail['quote count'] = tag_count #Tag count is the same as quote count
        details.append(detail)
    print(json.dumps(details, indent=5, ensure_ascii=False))
    return jsonify(details=details)








@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
