__all__ = ["get_poll_info", "get_registration"]

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

abbrs = {"AVE":"AVENUE","BOUL": "BOULEVARD","CT":"COURT","DR":"DRIVE","LN":"LANE","PL":"PLACE","PK":"PARK","RD": "ROAD","ST": "STREET","SQ": "SQUARE", "TERR": "TERRACE", "TER": "TERRACE", "WY": "WAY"}

def parse_address(address):
    attrs = address.split(" ")
    data = {}
    for attr in attrs:
        if attr.isdigit() and data.get("form_s0_house") is None:
            data["form_s0_house"] = int(attr)
        if attr.lower() in ["north", "west", "east", "south"]:
            data["comboPrefix"] = attr.upper()
        if attr.upper() in ['no suffix', 'AVENUE', 'ALLEY', 'BOULEVARD', 'COURT', 'CIRCLE', 'DRIVE', 'HIGHWAY', 'HILL', 'LANE', 'LOOP', 'PLACE', 'PLAZA', 'PARK', 'ROAD', 'ROW', 'STREET', 'SQUARE', 'TERRACE', 'WAY', 'WALK']:
            data["comboType"] = attr.upper()
        elif attr.upper() in abbrs.keys():
            data["comboType"] = abbrs[attr.upper()]
        else:
            data["form_s0_street"] = attr

    if data.get("comboPrefix") is None:
        data["comboPrefix"] = "no prefix"
    if data.get("comboType") is None:
        data["comboType"] = "no suffix"

    return data

def get_request(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    first_form = soup.find_all("form")[0]
    action = first_form.attrs.get("action").lower()
    url = urllib.parse.urljoin(url, action)
    return url, first_form

def get_poll_info(url, line1, zip):
    url, first_form = get_request(url)
    data = parse_address(line1)
    data["form_s0_zip"] = zip
    res = requests.post(url, data=data)

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        poll = str(soup.strong).replace('<br/>', '\n')
        poll_soup = BeautifulSoup(poll, "html.parser")
        name, address = tuple(poll_soup.strong.text.split("\n"))
        txt = soup.find_all("center")[-1].text
        hours = re.findall("from .* to .*", txt)[0].replace("from ", "")
        return name, address, hours
    except:
        return "Could not find this address", ""

def get_registration(url, data):
    data["email"] = "a@a.com" #don't sign anyone up
    data["phone_number"] = ""
    url, first_form = get_request("https://verify.vote.org/")
    res = requests.post(url, data=data)

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.h2.text.strip()
    except:
        return "Your registration status could not be determined."
