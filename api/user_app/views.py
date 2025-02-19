from decouple import config
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.busstop_app.models import BusStop
from api.institution_app.models import Institution
from api.permissions import IsAdmin, IsStudent
from api.search import apply_search
from api.user_app.tasks import send_email_reset_password
from api.user_app.utils.token import get_tokens_for_user

from .filters import apply_filters_users
from .models import User, NumericToken
from .serializers import *
from .service import UserService
from .utils.add_user_to_group import add_user_to_group
from .utils.generate_numeric_token import generate_numeric_token

user_service = UserService()

def generate_token(user, device_type="web"):
    if device_type == "mobile":
        return generate_numeric_token(user)
    else:
        return default_token_generator.make_token(user)


# Create your views here.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def student_create_view(request, matric):
    serializer = UserStudentRegisterSerializer(data=request.data)

    if not user_service.is_student_in_list(matric):
        return Response(
            {"error": "Estudante não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    if serializer.is_valid():
        user = serializer.save()
        user.is_student = True
        user.save()

        add_user_to_group(user, "Student")

        tokens = get_tokens_for_user(user)
        data = {
            "message": "Student profile created successfully",
            "refresh_token": tokens["refresh"],
            "access_token": tokens["access"],
            "student": UserStudentSerializer(user).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def student_get_info_view(request):
    if request.method == "POST":
        serializer = UserStudentByMatricSerializer(data=request.data)

        if serializer.is_valid():
            student_info = user_service.get_user_in_students_list(
                serializer.validated_data["matric"]
            )

            if student_info:
                student_serializer = UserStudentFromJsonFileSerializer(student_info)

                data = {"student": student_serializer.data}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Estudante não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            student_profile,
            data=request.data,
            partial=True,
            context={"request": request},
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami_view(request):
    user = request.user
    serializer = UserStudentSerializer(user)
    data = {"user": serializer.data}

    return Response(data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password_view(request, user_uuid):
    if request.method == "PUT":
        user = get_object_or_404(User, id=user_uuid)

        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response(
                {"error": "As senhas não coincidem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request):
    if request.method == "POST":
        email = request.data.get("email")
        device = request.data.get("device", "web")
        try:
            user = User.objects.get(email=email)
            token = generate_token(user,device)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            if device == "web":
                reset_link = request.build_absolute_uri(f"/reset-password/{uid}/{token}/")
            else:
                reset_link = f"Código de redefinição: {token}"

            subject = "Redefinir senha"
            html_message = render_to_string(
                "password_reset_email.html", {"reset_link": reset_link, "device":device}
            )
            plain_message = strip_tags(html_message)
            from_email = config("EMAIL_HOST_USER")

            send_email_reset_password.delay(
                subject=subject,
                plain_message=plain_message,
                from_email=from_email,
                email=email,
                html_message=html_message,
            )

            return Response(
                {"message": "Email enviado com sucesso."}, status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Email não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            if not new_password or not confirm_password:
                return Response(
                    {"error": "As senhas não podem ser vazias."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if new_password != confirm_password:
                return Response(
                    {"error": "As senhas não coincidem."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_numeric_token_view(request):
    if request.method == "POST":
        numeric_token = request.data.get("numeric_token")
        email = request.data.get("email")

        if not numeric_token or not email:
            return Response({"error": "Email ou token não informados."},status=status.HTTP_400_BAD_REQUEST)
        
        if len(numeric_token) != 6:
            return Response({"error": "Token inválido. Deve conter 6 números."}, status=status.HTTP_400_BAD_REQUEST)  

        if numeric_token.isdigit() == False:
            return Response({"error": "Token inválido. Deve ser números."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = NumericToken.objects.get(user=user)
        except User.DoesNotExist:
            return Response(
                {"error": "Email não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except NumericToken.DoesNotExist:
            return Response(
                {"error": "Token não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
    
        is_valid, message = token.validate_token(numeric_token)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        token.delete()        
        return Response({"message": message}, status=status.HTTP_200_OK)
        
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def avatar_upload_view(request):
    if request.method == "PATCH":
        try:
            user = request.user
            student_profile = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Perfil de estudante não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        student_profile.avatar = request.data["avatar"]
        student_profile.save()

        return Response(
            {"message": "Avatar atualizado com sucesso."}, status=status.HTTP_200_OK
        )

    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_student_create_profile_view(request):
    if request.method == "POST":
        user = request.user
        serializer = UserStudentProfileCreateSerializer(data=request.data)
        try:
            institution = Institution.objects.get(name=request.data["institution"])
        except Institution.DoesNotExist:
            return Response(
                {"error": "Instituição não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            bus_stop = BusStop.objects.get(id=request.data["bus_stop"])
        except BusStop.DoesNotExist:
            return Response(
                {"error": "Ponto de ônibus não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if serializer.is_valid():
            serializer.save(user=user, institution=institution, bus_stop=bus_stop)

            data = {"message": "Student profile created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
