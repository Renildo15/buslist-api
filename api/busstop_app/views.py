from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrIsDriver

from .serializers import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bus_stop_list_view(request):
    if request.method == "GET":
        bus_stop = BusStop.objects.all()
        serializer = BusStopSerializer(bus_stop, many=True)

        data = {"bus_stop": serializer.data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminOrIsDriver])
def bus_stop_create_view(request):
    if request.method == "POST":
        serializer = BusStopCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"message": "Bus stop created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
