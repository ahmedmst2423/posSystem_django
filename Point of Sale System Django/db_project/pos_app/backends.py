from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import connection

class OperatorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pos_app_operator WHERE username = %s AND password = %s", [username, password])
            row = cursor.fetchone()

        if row:
            user_model = get_user_model()
            user = user_model.objects.filter(username=username).first()

            if user:
                return user

        return None
