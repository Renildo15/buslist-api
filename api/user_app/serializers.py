from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework import serializers

from api.institution_app.models import Institution

from .models import StudentProfile, User
from .validators import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_student",
            "is_driver",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserStudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate_username(self, value):
        request = self.context.get("request")
        user = request.user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Username já está em uso.")
        return value

    def validate_email(self, value):
        request = self.context.get("request")
        user = request.user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email já está em uso.")
        return value


class UserStudentFromJsonFileSerializer(serializers.Serializer):
    name_student = serializers.CharField(max_length=255)
    sex_student = serializers.CharField(max_length=1)
    matriculation_student = serializers.CharField(max_length=11)
    status_student = serializers.CharField(max_length=20)
    teaching_level_student = serializers.CharField(max_length=21)
    course_student = serializers.CharField(max_length=100)
    institution_student = serializers.CharField(max_length=100)


class UserStudentByMatricSerializer(serializers.Serializer):
    matric = serializers.CharField(max_length=11)


class UserStudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'password' deve conter ao menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número"
            )
        return make_password(value)

    email = serializers.EmailField(validators=[EmailValidator])
    first_name = serializers.CharField(validators=[validate_first_name])
    last_name = serializers.CharField(validators=[validate_last_name])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            return user


class UserStudentProfileUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[validate_phone_number], required=False
    )
    user = UserStudentUpdateSerializer()

    class Meta:
        model = StudentProfile
        fields = ["phone_number", "bus_stop", "user"]

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.bus_stop = validated_data.get("bus_stop", instance.bus_stop)

        user_data = validated_data.get("user")
        user = instance.user

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.save()

        instance.save()
        return instance


class UserStudentProfileCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])
    matric_number = serializers.CharField(validators=[validate_matric_number])
    sex = serializers.CharField(validators=[validate_sex])
    status = serializers.CharField(validators=[validate_status])
    teaching_level = serializers.CharField(validators=[validate_teaching_level])
    course_name = serializers.CharField(validators=[validate_course_name])
    bus_stop = serializers.CharField(required=False, allow_null=True)
    institution = serializers.CharField(required=False, allow_null=True)
    user = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        # Implementa a lógica para criar uma instância do StudentProfile
        return StudentProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Implementa a lógica para atualizar a instância existente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserStudentProfileSerializer(serializers.ModelSerializer):
    institution = serializers.StringRelatedField()
    bus_stop = serializers.StringRelatedField()

    class Meta:
        model = StudentProfile
        exclude = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )


class UserStudentSerializer(UserSerializer):
    profile = UserStudentProfileSerializer(source="studentprofile", read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile",)
