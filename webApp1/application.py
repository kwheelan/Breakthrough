import os

from flask import Flask, render_template, request
import requests

from formTools import *

app = Flask(__name__)

app.static_folder = 'static'

#api key for google civic api
API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

@app.route("/")
def index():
    """ home page """
    return render_template("index.html")

@app.route("/registration/query")
def registration_forms():
    """ page to enter info for registation"""
    return render_template("registrationForm.html")

@app.route("/registration/info", methods=["POST"])
def registration():
    """Get polling info."""

    data = {}

    #Name
    data["first_name"] = request.form.get("firstName")
    data["last_name"] = request.form.get("lastName")

    # Get address information.
    data["street_address"] = request.form.get("address")
    ## TODO: enable apartments
    data["apartment"] = ""
    data["city"] = request.form.get("city")
    data["state"] = request.form.get("state")
    data["zip_5"] = request.form.get("zip")

    #dob
    data["date_of_birth_month"] = 1#request.form.get("mon")
    data["date_of_birth_day"] = 1#request.form.get("day")
    data["date_of_birth_year"] = 2000#request.form.get("year")

#    return data

    text = get_registration("https://verify.vote.org/", data)
    return render_template("registration.html", text=text)

@app.route("/contact")
def contact():
    """ home page """
    return render_template("contact.html")

@app.route("/faqs")
def faqs():
    return "In progress"

@app.route("/poll_finder")
def pollFinder():
    """Get polling info."""

    # Get form information.
    line1 = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip = request.form.get("zip")

    if city.lower()=="san francisco":
        name, address, hours = get_poll_info("https://www.sfelections.org/tools/pollsite/", line1, zip)
        return render_template("info.html", name=name, line1=address, hours=hours)

    else:
        address = "{} {} {} {}".format(line1, city, state, zip)

        #HTTP request to API
        res = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo",
                           params={"address": address, "returnAllAvailableData": True,
                           "key": API_KEY})
        if res.status_code != 200:
            return "ERROR: Badly formatted address."
        data = res.json()
        try:
            location = data["pollingLocations"][0]["address"]["locationName"]
            line1 = data["pollingLocations"][0]["address"]["line1"]
        except:
            location = "No polling data for this address or no upcoming elections."
            line1 = ""
        try:
            hours = data["pollingLocations"][0]["pollingHours"]
        except:
            hours = "No available hours for this location"
        return render_template("info.html", name=location, line1=line1, hours=hours)
