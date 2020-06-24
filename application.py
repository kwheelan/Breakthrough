import os

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info", methods=["POST"])
def info():
    """Get polling info."""

    # Get form information.
    address = request.form.get("address")

    #HTTP request to API
    res = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo",
                       params={"address": address, "returnAllAvailableData": True,
                       "key": API_KEY})
    if res.status_code != 200:
        return "ERROR: Badly formatted address."
    data = res.json()
    try:
        location = data["pollingLocations"][0]["address"]["locationName"]
        #line1 = data["pollingLocations"][0]["address"]["locationName"]
    except:
        location = "No polling data for this address or no upcoming elections."
    try:
        hours = data["pollingLocations"][0]["pollingHours"]
    except:
        hours = "No available hours for this location"
    return render_template("info.html", location=location, hours=hours)
    #line1=line1, city=city, state=state, zip=zip)
