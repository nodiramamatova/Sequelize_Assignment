
## Step 4 - Climate App

#Now that you have completed your initial analysis, design a Flask api based on the queries that you have just developed.

#* Use FLASK to create your routes.

### Routes

#
# * Query for the dates and temperature observations from the last year.

#  * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

#  * Return the json representation of your dictionary.

#* `/api/v1.0/stations`

#  * Return a json list of stations from the dataset.

#* `/api/v1.0/tobs`

#  * Return a json list of Temperature Observations (tobs) for the previous year

#* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#  * Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or #start-end range.

#  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date #inclusive.
#############################################################################################################################

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Stations = Base.classes.stations
Measurements = Base.classes.measurements

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available API routs."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
     )   
# * `/api/v1.0/precipitation`

#  * Query for the dates and temperature observations from the last year.

#  * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

#  * Return the json representation of your dictionary.     
      
@app.route("/api/v1.0/precipitation")
def precipitation():
    dict = {}
    last_date =session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    year_before_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_obsr = session.query(Measurements.date, Measurements.tobs).filter(
                Measurements.date > year_before_date).order_by(Measurements.date).all() 


    tobs_totals =[]
    for result in temp_obsr:
        tobs_dict = {}
        tobs_dict["date"] = result[1]
        #tobs_dict["tobs"] = result[1]
        tobs_totals.append(tobs_dict)
	 
    return jsonify(tobs_totals)
	 
#######################################################################################	 
#* `/api/v1.0/stations`

#  * Return a json list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Stations.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


########################################################################################
# * `/api/v1.0/tobs`

#  * Return a json list of Temperature Observations (tobs) for the previous year  
@app.route("/api/v1.0/tobs")
def tobs():
    last_date =session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    year_before_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurements.date, Measurements.tobs).filter(
                Measurements.date > year_before_date).order_by(Measurements.date).all()
    all_temp = []
    
    temp_dict = {}
    for result in results:
        temp_dict["date"] = result[1]
        all_temp.append(temp_dict)
    #tobs_results = list(np.ravel(results[1]))
    return jsonify(all_temp)
    
                    
###################################################################################
# * `/api/v1.0/<start>
# *  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater
# than and equal to the start date.
@app.route("/api/v1.0/<start>")
def temp_start(start):
    max_min_avg_temp = session.query(
        func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(
        Measurements.date >= start).all()   
    return jsonify({'tmin': max_min_avg_temp[0][0], 'tavg': max_min_avg_temp[0][1], 'tmax': max_min_avg_temp[0][2]})
	 
######################################################################################################################                       
#/api/v1.0/<start>/<end>
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#for dates between the start and end date #inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    max_min_avg_temp = session.query(
        func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(
        Measurements.tobs)).filter(
        Measurements.date > start).filter(Measurements.date < end).all()
            
    return jsonify({"tmin": max_min_avg_temp[0][0], "tavg": max_min_avg_temp[0][1], "tmax": max_min_avg_temp[0][2]}) 

#######################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)


