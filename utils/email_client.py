from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from config import settings
import logging

logger = logging.getLogger(__name__)

async def send_email(to_email: str, subject: str, content: str) -> bool:
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        email = Mail(
            from_email=Email("noreply@dgh.cm", "DGH System"),
            to_emails=To(to_email),
            subject=subject,
            content=Content("text/plain", content)
        )
        response = sg.send(email)
        logger.info(f"Email sent to {to_email}, status: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False