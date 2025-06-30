from rest_framework import serializers


class WhatsAppSendMessageSerializer(serializers.Serializer):
    body = serializers.CharField()
    to = serializers.CharField(required=False, default="+380968372100")
    from_ = serializers.CharField(required=False, default="+14155238886")
