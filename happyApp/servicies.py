from rest_framework.authtoken.models import Token
from .models import UserModel


def create_tokens_for_existing_users():
    users = UserModel.objects.all()
    for user in users:
        Token.objects.get_or_create(user=user)
