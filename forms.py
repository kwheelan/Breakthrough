#https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python

__all__ = ["get_address"]

import requests
from bs4 import BeautifulSoup
import urllib.parse

#url = "https://www.sfelections.org/tools/pollsite/"
#url = "https://wikipedia.com/"
#url = "https://www.sos.ca.gov/elections/polling-place/"
url = "https://verify.vote.org/"

def get_all_forms(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    for input_tag in form.find_all("select"):
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": None, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def get_address(url):
    first_form = get_all_forms(url)[0]
    form_details = get_form_details(first_form)

    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden":
            # if it's hidden, use the default value
            data[input_tag["name"]] = input_tag["value"]
        elif input_tag["type"] != "submit":
            # all others except submit, prompt the user to set it
            value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
            data[input_tag["name"]] = value

    action = first_form.attrs.get("action").lower()
    url = urllib.parse.urljoin(url, form_details["action"])

    if form_details["method"] == "post":
        res = requests.post(url, data=data)
    elif form_details["method"] == "get":
        res = requests.get(url, params=data)

    # the below code is only for replacing relative URLs to absolute ones
    soup = BeautifulSoup(res.text, "html.parser")
    for link in soup.find_all("link"):
        try:
            link.attrs["href"] = urljoin(url, link.attrs["href"])
        except:
            pass
    for script in soup.find_all("script"):
        try:
            script.attrs["src"] = urljoin(url, script.attrs["src"])
        except:
            pass
    for img in soup.find_all("img"):
        try:
            img.attrs["src"] = urljoin(url, img.attrs["src"])
        except:
            pass
    for a in soup.find_all("a"):
        try:
            a.attrs["href"] = urljoin(url, a.attrs["href"])
        except:
            pass

    return soup.h2.text.strip()
    #write the page content to a file
    #open("page.html", "w").write(str(soup))

    # poll = str(soup.strong).replace('<br/>', '\n')
    # soup = BeautifulSoup(poll, "html.parser")
    # return tuple(soup.strong.text.split("\n"))

print(get_address(url))
#print("{}\n{}".format(name,address))
