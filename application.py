import os

from flask import Flask, render_template, request, session
import requests

from formTools import *
from datetime import date

app = Flask(__name__)
app.secret_key = '1k93khlj15jK'
app.static_folder = 'static'

#api key for google civic api
API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

#Helper functions
def registrationHelper():
    """Get registration information"""
    data = {}

    if request.method == "POST":
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
        for key in ['first_name', 'last_name',"street_address", "apartment", "city", "state", "zip_5"]:
            session[key] = data[key]

        name = "{} {}".format(data["first_name"], data["last_name"])
        address = "{}, {}, {} {}".format(data["street_address"], data["city"], data["state"], data["zip_5"])

        #dob
        data["date_of_birth_month"] = 1#request.form.get("mon")
        data["date_of_birth_day"] = 1#request.form.get("day")
        data["date_of_birth_year"] = 2000#request.form.get("year")

        text = get_registration("https://verify.vote.org/", data)
        session['registration_info'] = (text, name.title(), address.title())

    return session['registration_info']

def pollFinderHelper():
    """Helper method to get poll information"""

    # Get form information.
    if request.method == 'POST':
        line1 = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zip")
    elif request.method == 'GET':
        line1 = session["street_address"]
        city = session["city"]
        state = session["state"]
        zip = session["zip_5"]

    # if city.lower()=="san francisco":
    #     location, line1, hours = get_poll_info("https://www.sfelections.org/tools/pollsite/", line1, zip)
    # else:
    if True:
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
    return location, line1, hours

states = ["CA"]
stateLangDict = { "CA": ['zh', 'es'], "FL" : ['es']}
langDict = { "zh" : 'mandarin', "es": 'spanish', 'en': 'english'}
statePages = ['home', 'register', 'faqs']

def get_page(lang, state, page, national=False):
    """help method to fetch html file by state and language"""
    if state.upper() not in states or lang not in langDict.keys():
       return "PAGE NOT FOUND"
    if national:
        loc = 'national'
    else:
        loc = state.upper()
    return render_template(f"{loc}/{langDict[lang]}/{page}.html", langs=stateLangDict[state.upper()], state=state)

#National landing page
@app.route("/")
def index():
    return home('en', 'CA')
    # return render_template("index.html")

@app.route('/landing-page')
def land():
    election = date(2020, 11, 3)
    days_to_election = max(0, (election - date.today()).days)
    return render_template("index.html", langs = ['zh', 'es'], days_to_election = days_to_election)

#Home
@app.route("/<lang>/<state>/home")
def home(lang, state):
    return get_page(lang, state, 'home')

#Register to vote page
@app.route("/<lang>/<state>/register")
def register(lang,state):
    return get_page(lang, state, 'register')

#STATE FAQS
@app.route("/<lang>/<state>/faqs")
def faqs(lang,state):
    return get_page(lang, state, 'faqs')

@app.route("/<lang>/<state>/registration/query")
def registration_forms(lang, state):
    return get_page(lang, state, 'registrationForm', True)

@app.route("/<lang>/<state>/registration/info")
def registration(lang, state):
    return get_page(lang, state, 'registration', True)

@app.route("/<lang>/<state>/poll_finder/query")
def poll_forms(lang, state):
    return get_page(lang, state, 'poll_form', True)

@app.route("/<lang>/<state>/poll_finder/query")
def pollFinder(lang, state):
    return get_page(lang, state, 'poll_info', True)
