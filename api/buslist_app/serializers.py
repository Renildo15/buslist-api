from rest_framework import serializers

from api.user_app.serializers import UserStudentSerializer

from .models import *
from .validators import *


class BusListSerializer(serializers.ModelSerializer):
    students = UserStudentSerializer(many=True)

    class Meta:
        model = BusList
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get("exclude_students", False):
            representation = {
                "id": instance.id,
                "name": instance.name,
                "list_date": instance.list_date,
                "is_enable": instance.is_enable,
            }

        return representation


class BusListCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_name])
    shift = serializers.CharField(validators=[validate_shift])
    type_creation = serializers.CharField(validators=[validate_type_creation])

    class Meta:
        model = BusList
        fields = [
            "name",
            "list_date",
            "list_time_initial",
            "list_time_final",
            "shift",
            "type_creation",
        ]


class BusListStudentSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField()
    student = UserStudentSerializer()

    class Meta:
        model = BusListStudent
        fields = [
            "id",
            "student",
            "end_class_time",
            "is_return",
            "created_at",
            "updated_at",
        ]

    # def get_avatar(self, instance):
    #     student_profile = getattr(instance.student, 'studentprofile', None)
    #     if student_profile and student_profile.avatar:
    #         # request = self.context.get('request')
    #         # return request.build_absolute_uri(student_profile.avatar.url) if request else student_profile.avatar.url
    #         return student_profile.avatar.url
    #     return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get("exclude_id", False):
            representation = {
                "end_class_time": instance.end_class_time,
                "is_return": instance.is_return,
            }

        return representation


class BusListStudentCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusListStudent
        fields = ["end_class_time", "is_return"]


class NoticeSerilizer(serializers.ModelSerializer):
    buslist = serializers.StringRelatedField()

    class Meta:
        model = Notice
        fields = "__all__"


class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["title", "description"]
