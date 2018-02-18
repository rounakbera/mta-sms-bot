# Sending an SMS using the Twilio API
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

'''
# put your own credentials here
account_sid = "AC8816577cc14eec0b84cb97298837edb9"
auth_token = "f74851e59b188f810f96afaac52eabfe"

client = Client(account_sid, auth_token)
'''

def scrape_service_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    service_list = soup.findAll("a", {"class": "plannedWorkDetailLink"})
    # print(service_list[0].find("i"))
    return service_list

'''
def scrape_details_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    details = soup.findAll("b")
    return details
'''

@app.route('/')
def index():
   return '<html><body><h1>"Hello World"</h1></body></html>'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == '1':
        service_list = scrape_service_data('http://www.mta.info/status/subway/123/25315367')
        for i in range(len(service_list)):
            resp.message(get_subway_lines(service_list[i].findAll("img")) + " " + service_list[i].find("i").text + ": " + service_list[i].find("img").text)

    return str(resp)

def get_subway_lines(tag_list):
    return_str = ""
    for i in range(len(tag_list)):
        return_str += tag_list[i]["alt"] + " "
    return return_str


if __name__ == "__main__":
    asdf = scrape_service_data('http://www.mta.info/status/subway/123/25315367')
    # print(asdf[0].find("img").text)
    # app.run(debug=True)
