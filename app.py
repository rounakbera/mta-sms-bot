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
        service_list = scrape_data()
        resp.message(scrape_data()[2].findAll("img"))
        for i in service_list:
            message = Message()
            message.body = get_subway_lines(scrape_data()[i].findAll("img")) + " " + service_list[i].find("i").text
            resp.append(message)

    return str(resp)

def get_subway_lines(tag_list):
    return_str = ""
    for i in range(len(tag_list)):
        return_str += tag_list[i]["alt"] + " "
    return return_str

'''
print(scrape_data()[0].find("i").text)
print(scrape_data()[0].findAll("img"))
print(get_subway_lines(scrape_data()[0].findAll("img")))
'''


if __name__ == "__main__":
    app.run(debug=True)
