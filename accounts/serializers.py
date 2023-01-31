from accounts.models import Ticket
from rest_framework.serializers import ModelSerializer


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "title",
            "user_text",
        )
