import os

from flask import Flask, render_template, request, session
import requests

from formTools import *

app = Flask(__name__)
app.secret_key = '1k93khlj15jK'

app.static_folder = 'static'

#api key for google civic api
API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

@app.route("/")
def index():
    """ home page """
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

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
    name = "{} {}".format(data["first_name"], data["last_name"])

    # Get address information.
    data["street_address"] = request.form.get("address")
    ## TODO: enable apartments
    data["apartment"] = ""
    data["city"] = request.form.get("city")
    data["state"] = request.form.get("state")
    data["zip_5"] = request.form.get("zip")

    address = "{}, {}, {} {}".format(data["street_address"], data["city"], data["state"], data["zip_5"])

    for key in ["street_address", "apartment", "city", "state", "zip_5"]:
        session[key] = data[key]

    #dob
    data["date_of_birth_month"] = 1#request.form.get("mon")
    data["date_of_birth_day"] = 1#request.form.get("day")
    data["date_of_birth_year"] = 2000#request.form.get("year")

#    return data

    # Hide this
    # if data["first_name"].lower() == "sarah" and data['last_name'].lower() == "dean":
    #     return render_template('confirm.html')
    #
    text = get_registration("https://verify.vote.org/", data)
    return render_template("registration.html", text=text, name=name, address=address)

@app.route("/contact")
def contact():
    """ home page """
    return render_template("contact.html")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/reminders")
def remind():
    return render_template("progress.html")

@app.route("/poll_finder/query")
def poll_forms():
    """show polling forms"""
    return render_template("poll_form.html")

@app.route("/poll_finder/info", methods = ["POST", "GET"])
def pollFinder():
    """Get polling info."""

    # Get form information.
    if request.method == 'POST':
        line1 = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zip")
    if request.method == 'GET':
        line1 = session["street_address"]
        city = session["city"]
        state = session["state"]
        zip = session["zip_5"]

    if city.lower()=="san francisco":
        name, address, hours = get_poll_info("https://www.sfelections.org/tools/pollsite/", line1, zip)
        return render_template("poll_info.html", name=name, line1=address, hours=hours)

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
        return render_template("poll_info.html", name=location, line1=line1, hours=hours)

@app.route("/warning")
def warning():
    return render_template("warning.html")
