import logging
import os
from http.client import HTTPResponse

import requests
from django.conf import settings
from django.http.request import HttpRequest
from twilio.rest import Client

logger = logging.getLogger(__name__)


def make_valid_phone_number(phone_number):
    """
    Formats a phone number as a WhatsApp contact string.
    """
    if phone_number.startswith("whatsapp:"):
        return phone_number
    if phone_number[0] != "+":
        phone_number = f"+{phone_number}"
    return f"whatsapp:{phone_number}"


def send_whatsapp_reply(
    message_body: str, from_wa_number: str = "+14155238886", to_wa_number: str = "+380968327100"
) -> str:
    """
    Sends a WhatsApp message with the specified body using Twilio API.
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=message_body,
        from_=make_valid_phone_number(from_wa_number),
        to=make_valid_phone_number(to_wa_number),
    )
    return message.sid


def is_media_send(request: HttpRequest) -> tuple[str, str, bool]:
    """
    Extracts sender, message body, and media presence flag from a WhatsApp HTTP request.
    """
    sender = request.POST.get("From")
    body = request.POST.get("Body")
    num_media = int(request.POST.get("NumMedia", 0))
    return sender, body, num_media > 0


def get_media_data(request: HttpRequest) -> tuple[str, str]:
    media_url = request.POST.get("MediaUrl0")
    media_type = request.POST.get("MediaContentType0")
    return media_url, media_type


def fetch_media(media_url: str) -> HTTPResponse:
    """
    Fetches media content from a URL provided in the
    POST data of a Django HttpRequest using Twilio authentication.
    """
    return requests.get(media_url, auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN))


def get_file_name(media_url):
    """
    Generates a file path for a media file from its URL, ensuring the target directory exists.
    """
    filename = media_url.split("/")[-1] + ".jpg"
    save_dir = "media/whatsapp/"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    return file_path


def save_media(file_path, response, media_type):
    """
    Saves media content to the specified file path and logs the operation with the media type.
    """
    with open(file_path, "wb") as f:
        f.write(response.content)
    logger.info(f"Сохранено {file_path} ({media_type})")
