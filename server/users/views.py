from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import User
import json


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        user = User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
        )

        user.full_clean()
        user.save()

        return JsonResponse({"message": "Usuario creado"}, status=201)

    except ValidationError as e:
        return JsonResponse({"errors": e.message_dict}, status=400)

    except Exception as e:
        return JsonResponse({"error": "Error interno"}, status=500)


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({"error": "Usuario no existe"}, status=404)

        if not user.check_password(password):
            return JsonResponse({"error": "Password incorrecto"}, status=400)

        return JsonResponse({
            "message": "Login exitoso",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        })

    except Exception as e:
        return JsonResponse({"error": "Error interno"}, status=500)


def get_users(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    users = User.objects.all()

    data = []
    for user in users:
        data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
        })

    return JsonResponse(data, safe=False)


def get_user(request, user_id):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        user = User.objects.get(id=user_id)

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

        return JsonResponse(data)

    except User.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)
