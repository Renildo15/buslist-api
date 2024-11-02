from rest_framework import serializers

from api.user_app.serializers import UserStudentSerializer

from .models import *
from .validators import *


class BusListSerializer(serializers.ModelSerializer):
    students = UserStudentSerializer(many=True)

    class Meta:
        model = BusList
        fields = "__all__"


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
    class Meta:
        model = BusListStudent
        fields = "__all__"


class BusListStudentCreateSerializer(serializers.ModelSerializer):

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
