import time

from django.db import connection
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer


# Create your views here.
def health_check_view(request):
    health_status = {"status": "UP"}
    start_time = time.time()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status["database"] = "UP"
    except Exception as e:
        health_status["database"] = f"DOWN: {str(e)}"
        health_status["status"] = "DOWN"

    health_status["response_time"] = round(time.time() - start_time, 3)

    return JsonResponse(health_status)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
