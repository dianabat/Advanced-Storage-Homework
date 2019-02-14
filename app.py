
# Use Flask to create an `app` instance.
from flask import Flask
from flask import jsonify

import pandas as pd
from statistics import mean 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

# Use route decorators to define the following endpoints:
# * `/`, or your **index route**: This should return a simple string, such as `"Hello, world!"`, or `"Welcome to my API!"`
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to the Climate App! Availabile routes: /api/v1.0/precipitation ; /api/v1.0/stations ; /api/v1.0/tobs ; /api/v1.0/<start> ; /api/v1.0/<start>/<end>"

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Percipitation' page...")

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    
    return jsonify(results)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    
    stations = session.query(Station.name, Station.station).all()
    return jsonify(stations)

#Query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature' page...")
    
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").all()
    return jsonify(temperature)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start' page...")

    tempdates = session.query(Measurement.date, Measurement.tobs).filter( Measurement.date >= start ).all()

    return jsonify(min(tempdates), max(tempdates))
    #Couldn't figure out how to get the average calculation to work here
    #return jsonify(np.mean(tempdates))

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    print("Server received request for 'Start End' page...")

    tempdates = session.query(Measurement.date, Measurement.tobs).filter( Measurement.date >= start, Measurement.date < end ).all()

    return jsonify(min(tempdates), max(tempdates))
    #Couldn't figure out how to get the average calculation to work here
    #return jsonify(np.mean(tempdates))

# * Finally, add code at the bottom of the file that allows you to run the server from the command line with: `python app.py`.
if __name__ == "__main__":
    app.run(debug=True)