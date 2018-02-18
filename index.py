# Sending an SMS using the Twilio API
from twilio.rest import Client
import requests
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
    r = requests.get('http://www.mta.info/')
    print(r.status_code)

scrape_date()
