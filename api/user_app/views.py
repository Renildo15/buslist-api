from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdmin, IsStudent
from api.user_app.utils.token import get_tokens_for_user

from .models import User
from .serializers import *
from .service import UserService
from .utils.add_user_to_group import add_user_to_group
from .filters import apply_filters_users
from api.search import apply_search

# Create your views here.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def student_create_view(request):
    serializer = UserStudentRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_student = True
        user.save()

        tokens = get_tokens_for_user(user)
        data = {
            "message": "Student profile created successfully",
            "refresh_token": tokens['refresh'],
            "access_token": tokens['access'],
            "student": UserStudentSerializer(user).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def student_get_info_view(request):
    if request.method == 'POST':
        user_service = UserService()
        serializer = UserStudentByMatricSerializer(data=request.data)
        
        if serializer.is_valid():
            student_info = user_service.get_user_in_students_list(serializer.validated_data['matric'])
            
            if student_info:
                student_serializer = UserStudentFromJsonFileSerializer(student_info)
                
                data = {"student": student_serializer.data}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Estudante não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"message": "Method not allowed"}, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )




@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def student_profile_view(request, user_uuid):
    if request.method == "POST":
        user = User.objects.get(id=user_uuid)
        serializer = UserStudentProfileCreateSerializer(data=request.data)

        if serializer.is_valid():
            student_profile = serializer.save(user=user)
            student_profile.save()
            add_user_to_group(user, "Student")

            data = {"message": "Student profile created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        user = get_object_or_404(User, id=user_uuid)
        student_profile = user.studentprofile

        serializer = UserStudentSerializer(user)
        data = {"student": serializer.data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsStudent])
def student_profile_update_view(request, user_uuid):
    user = get_object_or_404(User, id=user_uuid)
    student_profile = user.studentprofile
    if request.method == "PATCH":
        serializer = UserStudentProfileUpdateSerializer(
            student_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            data = {"message": "Student profile updated successfully"}

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin])
def staff_get_all_users_view(request):
    if request.method == "GET":
        users = User.objects.all()
    
        users = apply_filters_users(users, request)
        search_query = request.query_params.get("search")
        users = apply_search(users, search_query)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(users, request)
        serializer = UserStudentSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
