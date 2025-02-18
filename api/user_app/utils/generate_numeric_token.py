import random
from ..models import NumericToken

def generate_numeric_token(user):
    numeric_token = str(random.randint(100000, 999999))
    token, created = NumericToken.objects.get_or_create(
        user=user,
        defaults={"encrypted_numeric_token": numeric_token}
    )
    if not created:
        token.encrypted_numeric_token = numeric_token
        token.save()
    return numeric_token