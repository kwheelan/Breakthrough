import os

from flask import Flask, render_template, request, session
import requests

from tools import *
from datetime import date

app = Flask(__name__)
app.secret_key = '1k93khlj15jK' #to enable sessions
app.static_folder = 'static'

#api key for google civic api (polling location/hours)
API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"
#api key for Google Maps
MAPS_API_KEY = "AIzaSyCjVH1q11RrdM74l9r70bjDfwvRpRnsbVo"


#Helper functions:
def registrationHelper():
    """helper method to fetch registration information"""
    data = {}

    if request.method == "POST":
        #Name
        data["first_name"] = request.form.get("firstName")
        data["last_name"] = request.form.get("lastName")

        # Get address information.
        data["street_address"] = request.form.get("address")
        ## TODO: enable apartments
        data["apartment"] = request.form.get("line2")
        data["city"] = request.form.get("city")
        data["state"] = request.form.get("state")
        data["zip_5"] = request.form.get("zip")
        for key in ['first_name', 'last_name',"street_address", "apartment", "city", "state", "zip_5"]:
            session[key] = data[key]

        name = "{} {}".format(data["first_name"], data["last_name"])
        address = "{} {}, {}, {} {}".format(data["street_address"], data["apartment"], data["city"], data["state"], data["zip_5"])

        #dob
        data["date_of_birth_month"] = 1#request.form.get("mon")
        data["date_of_birth_day"] = 1#request.form.get("day")
        data["date_of_birth_year"] = 2000#request.form.get("year")

        text = get_registration("https://verify.vote.org/", data)
        session['registration_info'] = (text, name.title(), address.title())
        session['addressList'] = 'reset'

    return session['registration_info']

def pollFinderHelper():
    """Helper method to get poll information"""

    # TODO: (1) add address Information
    #       (2) parse multiple polling places
    #       (3) confirm accuracy/comprhensiveness with current election

    # Get form information.
    if request.method == 'POST':
        line1 = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zip")
    elif request.method == 'GET':
        try:
            if session["addressList"] != 'reset':
                return session["addressList"]
        except:
            pass
        line1 = session["street_address"]
        city = session["city"]
        state = session["state"]
        zip = session["zip_5"]

    #Disabled san francisco because the site seems outdated; CA polling places will
    # change in response to Covid/VBM access

    # if city.lower()=="san francisco":
    #     location, line1, hours = get_poll_info("https://www.sfelections.org/tools/pollsite/", line1, zip)
    # else:

    address = "{} {} {} {}".format(line1, city, state, zip)

    #HTTP request to Google Civic API
    res = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo",
                       params={"address": address, "returnAllAvailableData": True,
                       "key": API_KEY})
    if res.status_code != 200: #shouldn't ever happen
        return "ERROR: Badly formatted address."
    data = res.json()

    try:
        addressList = [poll["address"] for poll in data["pollingLocations"]]
    except:
        addressList = []

    for i in range(len(addressList)):
        if data["pollingLocations"][i].get("pollingHours"):
            addressList[i]["hours"] = data["pollingLocations"][i].get("pollingHours")
        else:
            addressList[i]["hours"] = "No available hours for this location."

    session['addressList'] = addressList

    return addressList

#states with enabled pages
states = ["CA", "FL", "GA", "TX", "MN", "US"]
#translations avaible for each state (CA translations temporarily disabled)
stateLangDict = { "CA": ['en'], "FL" : ['en', 'es'], "GA": ['en', 'es'], "TX": ['en', 'es'], "MN": ['en', 'es'], "US": ['en']}
#language url extension
langDict = { "zh" : 'mandarin', "es": 'spanish', 'en': 'english'}
stateDict = {'ca':'California', 'fl':'Florida', 'ga': 'Georgia', 'tx': 'Texas', 'mn': 'Minnesota'}

def get_page(lang, state, page, national=False):
    """help method to fetch html file by state and language"""
    if state.upper() not in states or lang not in stateLangDict[state.upper()]:
       return "PAGE NOT FOUND"
    if national:
        loc = 'national'
    else:
        loc = state.upper()
    return render_template(f"{loc}/{langDict[lang]}/{page}.html", langs=stateLangDict[state.upper()], state=state, lang=lang)


#URL routes

@app.route("/")
def index():
    """National landing page"""
    return home('en','ca')
    days = max((date(2020,11,3) - date.today()).days, 0)
    return render_template('index.html', days_to_election = days, states = states, stateDict = stateDict, lang='en', state = "US")

@app.route("/<lang>/<state>/about")
def about(lang,state):
    """About this project"""
    return get_page(lang, state, 'about', True)

@app.route("/<lang>/<state>/state-site-list")
def sos_site_list(lang,state):
    """List of official websites"""
    return get_page(lang, state, 'sos_list', True)

@app.route("/<lang>/<state>/home")
def home(lang, state):
    """State-specific homepage"""
    if state.upper() not in states or lang not in stateLangDict[state.upper()]:
       return "PAGE NOT FOUND"
    return render_template(f"national/{langDict[lang]}/home.html", langs=stateLangDict[state.upper()], state=state, state_long=stateDict[state.lower()], lang=lang)

@app.route("/<lang>/<state>/register")
def register(lang,state):
    """Register to vote page; renders state and language speicific html files"""
    return get_page(lang, state, 'register')

@app.route("/<lang>/<state>/faqs")
def faqs(lang,state):
    """State specific FAQs"""
    return render_template(f"national/faqs.html", langs=stateLangDict[state.upper()], state=state, lang=lang, lang_full = langDict[lang])

@app.route("/<lang>/<state>/faqs/search", methods = ['POST', 'GET'])
def faq_search(lang, state):
    if request.method == 'GET':
        return faqs(lang, state)
    keyword = request.form.get("keyword")
    return render_template(f"national/faqs.html", langs=stateLangDict[state.upper()], state=state, lang=lang,  lang_full = langDict[lang], search=True, keyword=keyword)

@app.route("/<lang>/<state>/registration/query")
def registration_forms(lang, state):
    """Get registration info form page; available in the languages for each state"""
    return get_page(lang, state, 'check_registration', False)
    #return get_page(lang, state, 'registrationForm', True)

@app.route("/<lang>/<state>/registration/info", methods = ['POST', 'GET'])
def registration(lang, state):
    """"Returns and displays registration info. If 'GET' request, uses stored data (ie for translating the page)"""
    if state.upper() not in states or lang not in langDict.keys():
       return "PAGE NOT FOUND"
    else:
        loc = state.upper()
    text, name, address = registrationHelper()
    return render_template(f"national/{langDict[lang]}/registration.html", langs=stateLangDict[state.upper()], state=state, text=text, name=name, address=address)

@app.route("/<lang>/<state>/poll_finder/query")
def poll_forms(lang, state):
    """Get registration info form page; available in the languages for each state"""
    return get_page(lang, state, 'poll_form', True)

@app.route("/<lang>/<state>/poll_finder/info", methods = ['POST', 'GET'])
def pollFinder(lang, state):
    """"Returns and displays poll info. If 'GET' request, uses stored data
    (ie for translating the page or going directly from registration info page)"""
    if state.upper() not in states or lang not in langDict.keys():
       return "PAGE NOT FOUND"
    else:
        loc = state.upper()
    return render_template(f"national/{langDict[lang]}/poll_info.html", langs=stateLangDict[state.upper()], state=state, addressList=pollFinderHelper())

@app.route("/<lang>/<state>/privacy-policy")
def privacy_policy(lang, state):
    return render_template("national/english/privacy_policy.html", state = state, lang = lang, langs=stateLangDict[state.upper()],)
