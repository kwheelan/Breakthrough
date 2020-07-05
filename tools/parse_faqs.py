from bs4 import BeautifulSoup
import requests
import os

numbers = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']

def printFAQS(url, filename):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    #soup = BeautifulSoup(open('textCode.html').read(), 'html.parser')
    f = open(filename, 'w')
    for n in numbers:
        try:
            f.write("Q: {}\n".format(soup.find_all(id = "heading"+n)[0].text.replace('       ','').strip()))
            f.write("A: {}\n\n".format(soup.find_all(id = "collapse"+n)[0].text.replace('       ','').strip()))

        except:
             f.close()
             break

printFAQS(filename="CA_FAQS.txt", url="https://breakthrough-voting-initiative.herokuapp.com/faqs")
