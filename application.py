import os

from flask import Flask, render_template, request, session
import requests

from formTools import *

app = Flask(__name__)
app.secret_key = '1k93khlj15jK'

app.static_folder = 'static'

#api key for google civic api
API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

#National english
@app.route("/registration/query")
def registration_forms():
    """ page to enter info for registation"""
    return render_template("national/english/registrationForm.html")

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

    text = get_registration("https://verify.vote.org/", data)
    return render_template("national/english/registration.html", text=text, name=name, address=address)

@app.route("/poll_finder/query")
def poll_forms():
    """show polling forms"""
    return render_template("national/english/poll_form.html")

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
        return render_template("national/english/poll_info.html", name=name, line1=address, hours=hours)

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
        return render_template("national/english/poll_info.html", name=location, line1=line1, hours=hours)

#National chinese
@app.route("/man/registration/query")
def registration_forms_mandarin():
    """ page to enter info for registation"""
    return render_template("national/mandarin/registrationForm.html")

@app.route("/man/registration/info", methods=["POST"])
def registration_mandarin():
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

    text = get_registration("https://verify.vote.org/", data)
    return render_template("national/mandarin/registration.html", text=text, name=name, address=address)

@app.route("/man/poll_finder/query")
def poll_forms_mandarin():
    """show polling forms"""
    return render_template("national/mandarin/poll_form.html")

@app.route("/man/poll_finder/info", methods = ["POST", "GET"])
def pollFinder_mandarin():
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
        return render_template("national/mandarin/poll_info.html", name=name, line1=address, hours=hours)

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
        return render_template("national/mandarin/poll_info.html", name=location, line1=line1, hours=hours)


#CA english
@app.route("/")
def index():
    """ home page """
    return render_template("/CA/english/CA_home.html")

@app.route("/ca/register")
def register():
    return render_template("CA/english/register.html")

@app.route("/ca/faqs")
def faqs():
    return render_template("CA/english/faqs.html")

#CA chinese
@app.route("/man")
def CA_home_mandarin():
    return render_template("CA/mandarin/CA_home_mandarin.html")

@app.route("/man/ca/register")
def register_mandarin():
    return render_template("CA/mandarin/register.html")

@app.route("/man/ca/faqs")
def faqs_mandarin():
    return render_template("CA/mandarin/faqs.html")
