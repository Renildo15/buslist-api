from api.user_app.models import StudentProfile, User
from api.user_app.utils.students_list import get_students_list


class UserService:
    def get_user_in_students_list(self, matric_number):
        students_list = get_students_list()

        for student in students_list:
            if student["matriculation_student"] == matric_number:
                return student
        return None
