from api.user_app.models import StudentProfile, User
from api.user_app.utils.students_list import get_students_list


class UserService:

    def __init__(self):
        self.students_list = get_students_list()

    def get_user_in_students_list(self, matric_number):
        for student in self.students_list:
            if student["matriculation_student"] == matric_number:
                return student
        return None
    def is_student_in_list(self, matric_number):
        for student in self.students_list:
            if student["matriculation_student"] == matric_number:
                return True
        return False