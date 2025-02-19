from uuid import uuid4

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.busstop_app.models import BusStop
from api.institution_app.models import Institution

from cryptography.fernet import Fernet, InvalidToken

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_student = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group", related_name="user_custom_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="user_custom_permissions_set", blank=True
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class DriverProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "driver_profile"
        verbose_name = "Driver Profile"
        verbose_name_plural = "Driver Profiles"

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):

    SEX_CHOICES = (
        ("M", "M"),
        ("F", "F"),
    )

    STATUS_CHOICES = (
        ("ATIVO", "ATIVO"),
        ("CANCELADO", "CANCELADO"),
        ("CONCLUIDO", "CONCLUÍDO"),
    )

    TEACHING_LEVEL_CHOICES = (
        ("GRADUACAO", "GRADUAÇÃO"),
        ("POS_GRADUACAO", "PÓS-GRADUAÇÃO"),
        ("MESTRADO", "MESTRADO"),
        ("DOUTORADO", "DOUTORADO"),
        ("TECNICO", "TÉCNICO"),
        ("TECNICO_INTEGRADO", "TÉCNICO INTEGRADO"),
        ("FORMACAO_COMPLEMENTAR", "FORMAÇÃO COMPLEMENTAR"),
        ("LATU_SENSU", "LATU SENSU"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    matric_number = models.CharField(max_length=11, unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ATIVO")
    teaching_level = models.CharField(
        max_length=21, choices=TEACHING_LEVEL_CHOICES, default="GRADUACAO"
    )
    course_name = models.CharField(max_length=100)
    bus_stop = models.ForeignKey(
        BusStop, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_profile"
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.matric_number}"

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class NumericToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    encrypted_numeric_token = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="numeric_tokens")
    attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    token_created_at = models.DateTimeField(auto_now_add=True)
    token_expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "Numeric Token"
        verbose_name_plural = "Numeric Tokens"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['token_expires_at']),
        ]
    
    def __str__(self):
        return f'{self.user.first_name}'
            
    def save(self, *args, **kwargs):
        if not self.token_expires_at:
            self.token_expires_at = timezone.now() + timezone.timedelta(minutes=15)

        if not self.encrypted_numeric_token.startswith("gAAAA"):
            self.encrypted_numeric_token = cipher_suite.encrypt(self.encrypted_numeric_token.encode("utf-8")).decode("utf-8")

        super().save(*args, **kwargs)
    
    def get_decrypted_token(self):
        try:
            return cipher_suite.decrypt(self.encrypted_numeric_token.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            return None
    
    def increment_attempts(self):
        self.attempts += 1
        if self.attempts >= 5:
            self.is_blocked = True
        self.save(update_fields=['attempts', 'is_blocked'])

    def is_valid(self):
        return not self.is_blocked and timezone.now() <= self.token_expires_at
    
    def validate_token(self, token):
        if self.is_blocked:
            message = "Token bloqueado por excesso de tentativas. Gere um novo token."
            self.delete()
            return False, message
        if self.get_decrypted_token() != token:
            self.increment_attempts()
            return False, "Token inválido."
        if not self.is_valid():
            message = "Token expirado."
            self.delete()
            return False, message
        return True, "Token válido."