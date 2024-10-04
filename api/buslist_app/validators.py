import re

from rest_framework import serializers

from .models import *


def validate_name(name):
    if len(name) < 3:
        raise serializers.ValidationError("Name must be at least 3 characters long")
    return name


def validate_shift(shift):
    shift_list = [choice[0] for choice in BusList.SHIFT_CHOICES]

    if shift not in shift_list:
        raise serializers.ValidationError("Invalid shift")
    return shift


def validate_type_creation(type_creation):
    type_creation_list = [choice[0] for choice in BusList.TYPE_CREATION_CHOICES]

    if type_creation not in type_creation_list:
        raise serializers.ValidationError("Invalid type creation")
    return type_creation
