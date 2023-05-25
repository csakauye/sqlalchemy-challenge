# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# Creating engine 
engine = create_engine("sqlite:///SurfsUp///Resources///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Creating the homepage with all the api routes listed 
@app.route("/")
def homepage():
    """All available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end><br/>"
    )

# Getting the query results for precipitation over the last 12 months and making it into a dictionary to jsonify
@app.route("/api/v1.0/precipitation")
def precipitation():
    sel = [Measurement.date, Measurement.prcp]
    precip_date = session.query(*sel).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()

    precip = []
    for date, prcp in precip_date:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

# Getting a list of all the stations
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.station).all()
    
    station_list = list(np.ravel(station_names))

    return jsonify(station_list)

# Querying the dates and temperatures from the most active station over the last 12 months and making it into a list
@app.route("/api/v1.0/tobs")
def tobs():
    sel_2 = [Measurement.date, Measurement.tobs]
    temp_date = session.query(*sel_2).filter(Measurement.station == 'USC00519281').filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()

    tobs = list(np.ravel(temp_date))

    return jsonify(tobs)

# Querying the minimum, maximum and average temperature for dates equal to and greater than the specified start date 
@app.route("/api/v1.0/start/<start>")
def start(start):
    sel_3 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    start = "' '"

    start_query = session.query(*sel_3).filter(Measurement.date >= start).all()

    start_print = list(np.ravel(start_query))

    return jsonify(start_print)

# Querying the minimum, maximum and average temperature for dates in the specified date range (start-end)
@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):
    sel_4 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    start = "' '"

    end = "' '"

    start_end_query = session.query(*sel_4).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    start_end_print = list(np.ravel(start_end_query))

    return jsonify(start_end_print)

# Closing out the session         
session.close()

if __name__ == '__main__':
    app.run(debug=True)