# import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Create engine to hawaii.sqlite
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# Declare a Base
Base = automap_base()
# reflect an existing database into a new model
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# imports for Flask
from flask import Flask, jsonify

# Creating the app.
app = Flask(__name__)

# Define the initial index route.
# Home page.
# List all routes that are available.
@app.route("/")
def home():
    print("Server recieved request for \'Home\' page...")
    return (f"Welcome to my \'Home\' page! <br/>"
    f"Here are some of the possible paths you could take: <br/>"
    f"For Hawaii preciptiation data goto: /api/v1.0/precipitation <br/>"
    f"For a list of weather stations: /api/v1.0/stations <br/>"
    f"For the last 12 month temperature data from the most active station: /api/v1.0/tobs <br/>"
    f"Temperature statistics from the start date (yyyy-mm-dd) try: /api/v1.0/yyyy-mm-dd <br/>"
    f"Temperature statistics from start to end dates in format (yyyy-mm-dd) /api/v1.0/yyyy-mm-dd/yyyy-mm-dd <br/>"
    )


# Precipitation path
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary#
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precip_query = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precip_data = []
    for date, prcp in precip_query:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp  
        precip_data.append(precip_dict) 
    return jsonify(precip_data)

# Stations Path
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_query = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    stations = []
    for station, name, lat, lng, ele in station_query:
        station_dict= {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_dict['Latitude'] = lat
        station_dict['Longitude'] = lng
        station_dict['Elevation'] = ele
        stations.append(station_dict)

    return jsonify(stations)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0][0]
    most_active_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).all() 
    session.close()
    most_active_tobs = []
    for date, tobs in most_active_query:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['TOBS'] = tobs
        most_active_tobs.append(tobs_dict)
    return jsonify(most_active_tobs)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
@app.route("/api/v1.0/<start>")
def start_tobs(start):
    session = Session(engine)
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    start_data = []
    for min, avg, max in start_query:
        start_dict = {}
        start_dict['Minimum TOBS'] = min
        start_dict['Average TOBS'] = avg
        start_dict['Maximum TOBS'] = max
        start_data.append(start_dict)
    return jsonify(start_data)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def end_tobs(start,end):
    session = Session(engine)
    end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    end_data = []
    for min, avg, max in end_query:
        end_dict = {}
        end_dict['Minimum TOBS'] = min
        end_dict['Average TOBS'] = avg
        end_dict['Maximum TOBS'] = max
        end_data.append(end_dict)
    return jsonify(end_data)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)