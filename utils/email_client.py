import smtplib
from email.mime.text import MIMEText
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

async def send_email(email: str, subject: str, message: str) -> bool:
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = settings.SMTP_USER
    msg['To'] = email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT)) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
        logger.info(f"Email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False