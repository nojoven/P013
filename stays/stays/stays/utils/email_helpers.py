import requests
from stays.settings import ADMIN_EMAIL, EMAIL_HOST_USER, EMAIL_HOST, MAILGUN_API_KEY, DEFAULT_EMAIL_DESTINATION, MAILGUN_DOMAIN_NAME
from icecream import ic


def send_password_reset_email(**kwargs):
    return requests.post(
        f"https://api.mailgun.net/v3/{kwargs.get('domain_name')}/messages",
        auth=("api", kwargs.get("api_key")),
        data={
            "from": f"Admin User <{kwargs.get('from_email')}>",
            "to": [kwargs.get("destination_email")],
            "subject": "Password Reset",
            "text": f'Cliquez sur le lien suivant pour réinitialiser votre mot de passe: {kwargs.get("recovery_url")}'
        }
    )


def send_contact_form_message(**kwargs):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Admin User <{EMAIL_HOST_USER}>",
            "to": [ADMIN_EMAIL],
            "subject": "Password Reset",
            "text": f'Cliquez sur le lien suivant pour réinitialiser votre mot de passe: {recovery_url}'
        }
    )