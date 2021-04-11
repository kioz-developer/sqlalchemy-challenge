from flask import Flask, jsonify
from model import Model

app = Flask(__name__)

# Create model only one time
model = Model()

@app.route("/")
def home():
    #List all available api routes.
    return (
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = model.precipitation()
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = model.stations()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    results = model.last_year_tobs()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def tobs_by_start(start):
    results = model.tobs_by_start(start)
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def tobs_by_start_end(start, end):
    results = model.tobs_by_start_end(start, end)
    return jsonify(results)
