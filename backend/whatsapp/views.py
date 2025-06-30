import logging

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WhatsAppSendMessageSerializer
from .services import process_whatsapp_send_message, process_whatsapp_webhook

logger = logging.getLogger(__name__)


class WhatsAppSendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info("WhatsAppSendMessageView method post called")
        serializer = WhatsAppSendMessageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                sid = process_whatsapp_send_message(serializer.validated_data)
                return Response({"sid": sid}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Ошибка отправки WhatsApp: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def whatsapp_webhook(request):
    """
    Handles incoming WhatsApp webhook requests.
    Processes POST requests containing WhatsApp messages and returns an appropriate HTTP response.
    """
    if request.method == "POST":
        process_whatsapp_webhook(request)
        return HttpResponse("OK", status=200)
    return HttpResponse("Only POST", status=405)
