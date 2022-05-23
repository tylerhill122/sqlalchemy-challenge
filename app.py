import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify

# SQLAlchemy engine creation
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd (start date)<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (start date / end date)"
    )

recent_date = "2017-08-23"
recent_date_dt = datetime.strptime(recent_date, "%Y-%m-%d")
time_delta = recent_date_dt - timedelta(days=366)

### - Precipitation Flask Route - ###
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= time_delta).\
        order_by(Measurement.date.asc()).all()

    session.close()

    precip = []
    for date, prcp in query:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

### - Stations Flask Route - ###
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    query = session.query(Station.station).all()
    session.close()
    
    return jsonify(query)

### - Tobs Flask Route - ###
@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    query = session.query(Measurement.tobs).\
        order_by(Measurement.date).\
        filter(Measurement.date >= time_delta).\
        filter(Measurement.station == "USC00519281").all()
    
    session.close()
    return jsonify(query)

### - Variable Flask Route, Start - ###
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    date = func.date(Measurement.date)
    tmin = func.min(Measurement.tobs)
    tavg = func.avg(Measurement.tobs)
    tmax = func.max(Measurement.tobs)
    
    
    query = session.query(tmin, tavg, tmax).\
        filter(date >= start).all()
    session.close()
    
    temps = []
    for min,avg,max in query:
        temp_dict = {}
        temp_dict["Min"] = min
        temp_dict["Avg"] = avg
        temp_dict["Max"] = max
        temps.append(temp_dict)
    
    return jsonify(temps)

# ### - Variable Flask Route, Start/End - ###
# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
#     session = Session(engine)
    
#     tmin = func.min(Measurement.tobs)
#     tavg = func.avg(Measurement.tobs)
#     tmax = func.max(Measurement.tobs)
    
#     query = session.query(tmin, tavg, tmax).\
#         filter(Measurement.date >= start).\
#         filter(Measurement.date <= end).all()
#     session.close()
    
#     temps = []
#     for min,avg,max in query:
#         temp_dict = {}
#         temp_dict["Min"] = min
#         temp_dict["Avg"] = avg
#         temp_dict["Max"] = max
#         temps.append(temp_dict)
    
#     return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)