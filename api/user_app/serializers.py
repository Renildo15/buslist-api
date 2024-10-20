from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import StudentProfile, User
from .validators import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_student",
            "is_driver",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserStudentFromJsonFileSerializer(serializers.Serializer):
    name_student = serializers.CharField(max_length=255)
    sex_student = serializers.CharField(max_length=1)
    matriculation_student = serializers.CharField(max_length=11)
    status_student = serializers.CharField(max_length=20)
    teaching_level_student = serializers.CharField(max_length=21)
    course_student = serializers.CharField(max_length=100)


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


class UserStudentProfileCreateSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(validators=[validate_avatar])
    phone_number = serializers.CharField(validators=[validate_phone_number])
    matric_number = serializers.CharField(validators=[validate_matric_number])
    sex = serializers.CharField(validators=[validate_sex])
    status = serializers.CharField(validators=[validate_status])
    teaching_level = serializers.CharField(validators=[validate_teaching_level])
    course_name = serializers.CharField(validators=[validate_course_name])

    class Meta:
        model = StudentProfile
        fields = [
            "user",
            "avatar",
            "institution",
            "phone_number",
            "matric_number",
            "sex",
            "status",
            "teaching_level",
            "course_name",
            "bus_stop",
        ]


class UserStudentProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(validators=[validate_avatar], required=False)
    phone_number = serializers.CharField(
        validators=[validate_phone_number], required=False
    )

    class Meta:
        model = StudentProfile
        fields = [
            "avatar",
            "phone_number",
            "bus_stop",
        ]

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.bus_stop = validated_data.get("bus_stop", instance.bus_stop)
        instance.save()
        return instance


class UserStudentProfileSerializer(serializers.ModelSerializer):
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
