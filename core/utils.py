from rest_framework.authtoken.models import Token


def get_or_create_token(user):
    token = Token.objects.get_or_create(user=user)
    return token[0].key



