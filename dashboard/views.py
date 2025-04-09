from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(["POST"])
def receiveLogs(request):
    data = request.data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "log_group",
        {
            "type": "send_log",
            "data": data
        }
    )
    return Response({"message": "Data sent via WebSocket"})
