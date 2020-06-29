import os

from flask import Flask, render_template, request
import requests

from formTools import *

app = Flask(__name__)

app.static_folder = 'static'

#API_KEY = "AIzaSyB_TMYCnCqQz_UDRc6wsu7Tw7rMUbgQ0hQ"

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
