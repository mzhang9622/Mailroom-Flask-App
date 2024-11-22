from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_email(subject, to_email, html_content):
    """
    Sends an email using SendGrid.
    """
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        raise ValueError("SendGrid API key is not set.")

    message = Mail(
        from_email='mzhang9622@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email sent: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
