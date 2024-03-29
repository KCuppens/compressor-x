import logging
import os

from mailjet_rest import Client

from apps.config.models import Config

from .models import EmailTemplate


logger = logging.getLogger(__name__)


def send_email(key_name, to_name, to_email, params={}):  # noqa: B006
    mailjet = Client(
        auth=(
            os.environ["MJ_APIKEY_PUBLIC"],
            os.environ["MJ_APIKEY_PRIVATE"],
        ),
        version="v3.1",
    )
    if mailjet:
        email_template = EmailTemplate.objects.filter(key_name=key_name).first()
        sender_email = Config.objects.get_config("SENDER_EMAIL")
        sender_name = Config.objects.get_config("SENDER_NAME")
        template = fill_in_merge_tags(params, email_template.template)

        data = {
            "Messages": [
                {
                    "From": {"Email": sender_email, "Name": sender_name},
                    "To": [{"Email": to_email, "Name": to_name}],
                    "Subject": email_template.title,
                    "HTMLPart": template,
                }
            ]
        }
        mailjet.send.create(data=data)
        logger.info(f"Send email with: {data}")
        return "Email has been sent."
    return "Email requires api keys."


def fill_in_merge_tags(params, template):
    if len(params):
        for key, value in params.items():
            if key in template:
                template = template.replace(key, value)
    return template
