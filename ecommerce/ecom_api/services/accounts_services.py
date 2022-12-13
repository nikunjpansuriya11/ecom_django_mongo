from core.models import User

def check_email_existence(email=None):
    user_object = User.objects.filter(email=email)
    if user_object:
       return None
    else:
        return user_object
