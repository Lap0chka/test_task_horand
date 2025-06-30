from django.urls import path
from .views import WhatsAppSendMessageView, whatsapp_webhook

urlpatterns = [
    path("send-message/", WhatsAppSendMessageView.as_view(), name="whatsapp_send_message"),
    path("webhook/", whatsapp_webhook, name="whatsapp_webhook"),
]
