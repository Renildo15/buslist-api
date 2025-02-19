from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrIsDriver, IsStudent
from api.search import (apply_search, apply_search_notices,
                        apply_search_students)
from api.user_app.models import User

from .filters import *
from .models import *
from .serializers import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bus_list_enable_list_view(request):
    if request.method == "GET":

        date = request.query_params.get("date")
        bus_list = BusList.objects.filter(is_enable=True)

        if date:
            bus_list = bus_list.filter(list_date=date)

        bus_list = apply_filters_bus_list(bus_list, request)
        search_query = request.query_params.get("search")
        bus_list = apply_search(bus_list, search_query)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(bus_list, request)

        serializer = BusListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrIsDriver])
def bus_list_get_all_view(request):
    if request.method == "GET":
        bus_list = BusList.objects.all()

        bus_list = apply_filters_bus_list(bus_list, request)
        search_query = request.query_params.get("search")
        bus_list = apply_search(bus_list, search_query)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(bus_list, request)
        serializer = BusListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminOrIsDriver])
def bus_list_create_view(request):
    if request.method == "POST":
        buslists = BusList.objects.filter(is_enable=True).count()
        serializer = BusListCreateSerializer(data=request.data)
        if serializer.is_valid():
            if buslists >= 3:
                return Response(
                    {"message": "Você já possui 3 listas de ônibus ativas hoje"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            data = {"message": "Bus list created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdminOrIsDriver])
def bus_list_enable_disable_view(request, bus_list_id):
    bus_list = get_object_or_404(BusList, id=bus_list_id)
    if request.method == "PATCH":
        bus_list.is_enable = not bus_list.is_enable
        bus_list.save()
        data = {"message": "Bus list updated successfully"}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
def bus_list_student_create_view(request, bus_list_id, student_id):
    bus_list = get_object_or_404(BusList, id=bus_list_id)
    student = get_object_or_404(User, id=student_id)
    serializer = BusListStudentCreateAndUpdateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(bus_list=bus_list, student=student)
        data = {
            "message": "Bus list student created successfully",
        }

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsStudent])
def bus_list_remove_student_view(request, bus_list_id, student_id):
    bus_list = get_object_or_404(BusList, id=bus_list_id)
    student = get_object_or_404(User, id=student_id)
    bus_list_student = BusListStudent.objects.get(bus_list=bus_list, student=student)
    bus_list_student.delete()
    data = {
        "message": "Bus list student removed successfully",
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def buslist_student_list_view(request, buslist_id):
    if request.method == "GET":

        try:
            buslist = BusList.objects.get(id=buslist_id)
        except BusList.DoesNotExist:
            return Response(
                {"message": "Not found buslist"}, status=status.HTTP_404_NOT_FOUND
            )

        buslistStudents = BusListStudent.objects.filter(bus_list=buslist)
        buslistStudents = apply_filters_students(buslistStudents, request)
        search_query = request.query_params.get("search")
        buslistStudents = apply_search_students(buslistStudents, search_query)

        if buslistStudents.exists():
            serializers = BusListStudentSerializer(buslistStudents, many=True)

            data = {"students": serializers.data}

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Not found list"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsStudent])
def buslist_student_update_view(request, buslist_student_id):
    buslist_student = get_object_or_404(BusListStudent, id=buslist_student_id)
    if request.method == "PATCH":
        serializer = BusListStudentCreateAndUpdateSerializer(
            buslist_student, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            data = {"message": "Buslist student updated successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def buslist_student_detail_view(request, buslist_student_id):
    buslist_student = get_object_or_404(BusListStudent, id=buslist_student_id)
    if request.method == "GET":
        serializer = BusListStudentSerializer(buslist_student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated, IsAdminOrIsDriver])
def notice_create_list_view(request, bus_list_id):
    bus_list = get_object_or_404(BusList, id=bus_list_id)
    if request.method == "POST":
        serializer = NoticeCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(buslist=bus_list, created_by=request.user)
            data = {
                "message": "Notice created successfully",
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        notice = Notice.objects.filter(buslist=bus_list)
        serializer = NoticeSerilizer(notice, many=True)
        data = {"notice": serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notice_list_all_view(request):
    if request.method == "GET":
        user = request.user
        notices = Notice.objects.filter(buslist__students=user)

        notices = apply_filters_notice(notices, request)
        search_query = request.query_params.get("search")
        notices = apply_search_notices(notices, search_query)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(notices, request)
        serializer = NoticeSerilizer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notice_get_view(request, notice_id):
    if request.method == "GET":
        notice = get_object_or_404(Notice, id=notice_id)
        serializer = NoticeSerilizer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsStudent])
def notice_viewed_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == "PATCH":
        notice.viewed = True
        notice.save()

        data = {
            "message": "Notice updated successfully",
        }

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def buslist_detail_view(request, buslist_id):
    if request.method == "GET":
        try:
            buslist = BusList.objects.get(id=buslist_id)
        except BusList.DoesNotExist:
            return Response(
                {"message": "Not found buslist"}, status=status.HTTP_404_NOT_FOUND
            )
        buslist_serializer = BusListSerializer(
            buslist, context={"exclude_students": True}
        )
        return Response(buslist_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
