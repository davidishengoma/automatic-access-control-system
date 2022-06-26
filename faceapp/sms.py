

from twilio.rest import Client

from settings import settings


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_sms(to: str, msg: str):
    
    for t in to.split(","):
        message = client.messages \
                    .create(
                        body=msg,
                        from_='+19302031916',
                        to=t.strip()
                    )
        print(f"Sending sms to "+t)
