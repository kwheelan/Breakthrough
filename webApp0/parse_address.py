__all__ = ["get_poll_info"]

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

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
        else:
            data["form_s0_street"] = attr


    if data.get("comboPrefix") is None:
        data["comboPrefix"] = "no prefix"
    if data.get("comboType") is None:
        data["comboType"] = "no suffix"

    return data

def get_poll_info(url, line1, zip):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    first_form = soup.find_all("form")[0]

    action = first_form.attrs.get("action").lower()
    url = urllib.parse.urljoin(url, action)

    data = parse_address(line1)
    data["form_s0_zip"] = zip

    res = requests.post(url, data=data)

    # the below code is only for replacing relative URLs to absolute ones
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

# address = input("address: ")
# print(get_poll_info("https://www.sfelections.org/tools/pollsite/", address))
