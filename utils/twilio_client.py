from twilio.rest import Client
from config.settings import settings
import logging

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
logger = logging.getLogger(__name__)

async def send_sms(phone_number: str, message: str) -> bool:
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logger.info(f"SMS sent to {phone_number}, SID: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False

async def send_ivr(phone_number: str, message: str) -> bool:
    try:
        call = twilio_client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",  # i will Replace with TwiML URL
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER
        )
        logger.info(f"IVR call initiated to {phone_number}, SID: {call.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to initiate IVR: {e}")
        return False