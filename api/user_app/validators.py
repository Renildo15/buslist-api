import re

from rest_framework import serializers

from .models import StudentProfile


def validate_first_name(first_name):
    if len(first_name) < 3:
        raise serializers.ValidationError(
            "First name must be at least 3 characters long"
        )
    return first_name


def validate_last_name(last_name):
    if len(last_name) < 3:
        raise serializers.ValidationError(
            "Last name must be at least 3 characters long"
        )
    return last_name


def validate_phone_number(phone_number):
    pattern = r"^\(\d{2}\) \d{4,5}-\d{4}$"
    if not re.match(pattern, phone_number):
        raise serializers.ValidationError(
            "Phone number must be in the format (xx) xxxx-xxxx or (xx) xxxxx-xxxx"
        )
    return phone_number


def validate_matric_number(matric_number):
    pattern = r"^\d{11}$"
    if not re.match(pattern, matric_number):
        raise serializers.ValidationError("Matriculation number must have 11 digits")
    return matric_number


def validate_sex(sex):
    sex_list = [choice[0] for choice in StudentProfile.SEX_CHOICES]

    if sex.upper() not in sex_list:
        raise serializers.ValidationError("Sex must be M or F")
    return sex


def validate_status(status):
    status_list = [choice[0] for choice in StudentProfile.STATUS_CHOICES]

    if status.upper() not in status_list:
        raise serializers.ValidationError(
            "Status must be ATIVO, CANCELADO or CONCLUIDO"
        )
    return status


def validate_teaching_level(teaching_level):
    teaching_level_list = [
        choice[0] for choice in StudentProfile.TEACHING_LEVEL_CHOICES
    ]

    if teaching_level.upper() not in teaching_level_list:
        raise serializers.ValidationError(
            "Teaching level must be GRADUACAO, POS_GRADUACAO, MESTRADO, DOUTORADO, TECNICO, TECNICO_INTEGRADO, FORMACAO_COMPLEMENTAR or LATU_SENSU"
        )
    return teaching_level


def validate_avatar(avatar):
    limit = 100 * 1024 * 1024
    if avatar.size > limit:
        raise serializers.ValidationError("Avatar size must be less than 100MB")
    return avatar


def validate_course_name(course_name):
    if len(course_name) < 3:
        raise serializers.ValidationError(
            "Course name must be at least 3 characters long"
        )
    return course_name
