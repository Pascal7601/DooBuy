import resend
import os
from dotenv import load_dotenv


load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')
def send_registration_email(email: str, username: str):
  params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": [email],
    "subject": "email registration",
    "html": f"<h2>Welcome {username}to doobuy, a commercial website</h2>"
  }

  try:
    response = resend.Emails.send(params)
    print(f"email was sent succesfully {response}")
  except Exception as e:
    print(f"error sending email: {e}")