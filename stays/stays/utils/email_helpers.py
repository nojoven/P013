import requests


def send_password_reset_email(**kwargs):
    return requests.post(
        f"https://api.mailgun.net/v3/{kwargs.get('domain_name')}/messages",
        auth=("api", kwargs.get("api_key")),
        data={
            "from": f"Admin User <{kwargs.get('from_email')}>",
            "to": [kwargs.get("destination_email")],
            "subject": "Password Reset",
            "text": f'Please click on the following link: {kwargs.get("recovery_url")}',
        },
    )


def send_contact_form_email(**kwargs):
    return requests.post(
        f"https://api.mailgun.net/v3/{kwargs.get('domain_name')}/messages",
        auth=("api", kwargs.get("api_key")),
        data={
            "from": kwargs.get("from_email"),
            "to": [kwargs.get("destination_email")],
            "subject": kwargs.get("subject"),
            "text": kwargs.get("message"),
        },
    )
