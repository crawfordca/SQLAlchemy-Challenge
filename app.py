import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

  
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-22').\
    filter(measurement.date <'2017-08-23').\
    order_by(measurement.date).all()

    annual_prcp = []
    
    for a in results:
        annual_dict = {}
        annual_dict['date'] = a.date
        annual_dict['prcp'] = a.prcp
        annual_data.append(annual_dict)
    
 
    return jsonify(annual_pecp)

@app.route("api/v1.0/stations")
def stations():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
     #Return a JSON list of stations from the dataset. 
    
    stations = engine.execute('SELECT * FROM station').fetchall()
    
    return jsonify(stations)



@app.route("/api/v1.0/tobs")
def tobs():
   # Create our session (link) from Python to the DB
    session = Session(engine)
    
   # Query the dates and temperature observations of the most active station for the last year of data.
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').\
                        filter(measurement.date >= prev_year).all()
        
    annual_tobs = []
    for t in results:
        annual_dict = {}
        annual_dict['date'] = t.date
        annual_dict['tobs'] = t.tobs
        annual_data.append(annual_tobs)
    
    return jsonify(annual_tobs)


@app.route("/api/v1.0/start")
def start():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= 'date').all()
    
    
    start = []
    for s in results:
        start_dict = {}
        start_dict['Start Date'] = date
        start_dict['TMIN'] = s.min
        start_dict['TMAX'] = s.max
        start_dict['TAVG'] = s.agv
        start_data.append(start)
    
    return jsonify(start)

    
@app.route("/api/v1.0/end")
def end():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
  
 results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= 'date').\
                filter(measurement.date <= 'end').all()
    end = []
    for e in results:
        start_dict = {}
        start_dict['Start Date'] = date
        start_dict['TMIN'] = e.min
        start_dict['TMAX'] = e.max
        start_dict['TAVG'] = e.agv
        start_data.append(end)
    
    return jsonify(end)
    
    
if __name__ == '__main__':
    app.run(debug=True)