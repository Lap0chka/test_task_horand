from backend.whatsapp.utils import (fetch_media, get_file_name, get_media_data,
                                    is_media_send, save_media,
                                    send_whatsapp_reply)


def process_whatsapp_webhook(request):
    """
    Processes incoming WhatsApp media from a request:
    retrieves media data, downloads and saves the file,
    and sends a confirmation reply.
    """
    sender, body, num_media = is_media_send(request)
    if num_media:
        media_url, media_type = get_media_data(request)
        response = fetch_media(media_url)
        file_path = get_file_name(media_url)
        save_media(file_path, response, media_type)
        send_whatsapp_reply(message_body="Фото збережено, дякуємо!", to_wa_number=sender)
    else:
        if body == "Привiт":
            send_whatsapp_reply(
                message_body="Вітаємо! Надішліть фото, щоб зберегти його.", to_wa_number=sender
            )


def process_whatsapp_send_message(data):
    """
    Sends a WhatsApp message using data from the
    provided dictionary and returns the message SID.
    """
    sid = send_whatsapp_reply(
        message_body=data["body"],
        from_wa_number=data.get("from_", None),
        to_wa_number=data.get("to", None),
    )
    return sid
