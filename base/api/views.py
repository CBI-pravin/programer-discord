
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
from base.api import serializers


@api_view(['GET'])
def getRouts(request):
    routes = [
        'GET /api/room',
        'GET /api/room/std',
        'GET /api/room/std/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRoom(request, pk):
    # pk = request.GET.get(q)
    rooms = Room.objects.get(id = pk)
    serializer = RoomSerializer(rooms, many = False)
    return Response(serializer.data)


@api_view(['GET'])
def getRooms(request):
    # pk = request.GET.get(q)
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data)