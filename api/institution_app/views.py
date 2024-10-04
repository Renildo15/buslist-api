from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdmin

from .serializers import *


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def institution_list_create(request):
    if request.method == "GET":
        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions, many=True)

        data = {"institutions": serializer.data}

        return Response(data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = InstitutionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"message": "Institution created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
