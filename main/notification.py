from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_SENDER = "+15137177026"
TWILIO_PHONE_RECIPIENT = "+4915757086879"


def send_text_notification(text):
    print("Using account SID:", TWILIO_ACCOUNT_SID)
    print("Using auth token:", TWILIO_AUTH_TOKEN)

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body=text)
