import json
import os

from django.conf import settings


def get_students_list():
    file_path = os.path.join(settings.BASE_DIR, "data", "students.json")

    with open(file_path, "r") as f:
        students = json.load(f)

        return students
