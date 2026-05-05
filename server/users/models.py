from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        password = self.password

        if len(password) < 8:
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres")

        if not any(c.isupper() for c in password):
            raise ValidationError("Debe tener al menos una mayúscula")

        if not any(c.islower() for c in password):
            raise ValidationError("Debe tener al menos una minúscula")

        if not any(c.isdigit() for c in password):
            raise ValidationError("Debe tener al menos un número")

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
