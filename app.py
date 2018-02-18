# Sending an SMS using the Twilio API
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# put your own credentials here
account_sid = "AC8816577cc14eec0b84cb97298837edb9"
auth_token = "f74851e59b188f810f96afaac52eabfe"

client = Client(account_sid, auth_token)

'''
client.messages.create(
  to="+13142584515",
  from_="+16463928126",
  body="FUCK YOU ROUNAK",
  media_url="https://climacons.herokuapp.com/clear.png")
'''

def scrape_data():
    r = requests.get('http://www.mta.info/status/subway/123/25315367')
    soup = BeautifulSoup(r.text, 'html.parser')
    service_list = soup.findAll("a", {"class": "plannedWorkDetailLink"})
    # print(service_list[0].find("i"))
    return service_list

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
        resp.message(scrape_data())

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
