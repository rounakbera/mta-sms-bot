# Sending an SMS using the Twilio API
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

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
   return '<html><body><h1>MTA 1, 2, 3 Train Service Change SMS bot</h1><p>This bot uses the Twilio API and data scrapes the MTA website to text the user about any service delays on either the 1, 2, or 3 train.</p><p>Simply text +1(646)-392-8126 with the number of the desired line (1, 2, or 3).</p><p>Made by Rounak Bera and Raymond Li</p></body></html>'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body in ['1', '2', '3']:
        service_list = scrape_service_data('http://www.mta.info/status/subway/123/25315367')
        subwayQuery = body + " " + "Subway"
        for i in range(len(service_list)):
            details_list = service_list[i].findAll("b")
            return_str = get_subway_lines(service_list[i].findAll("img"))
            for j in range(len(details_list)):
                return_str += details_list[j].text
            if(subwayQuery in return_str):
                resp.message(return_str)
        resp.message('More details: http://www.mta.info/status/subway/123/25315367')
    else:
        resp.message('This bot uses the Twilio API and data scrapes the MTA website to text the user about any service delays on either the 1, 2, or 3 train. Simply text +1(646)-392-8126 with the number of the desired line (1, 2, or 3). Made by Rounak Bera and Raymond Li.')

    return str(resp)

def get_subway_lines(tag_list):
    return_str = ""
    for i in range(len(tag_list)):
        return_str += tag_list[i]["alt"] + " "
    return return_str


if __name__ == "__main__":
    app.run(debug=True)
