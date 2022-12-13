
from django.contrib.auth import authenticate
from core.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import mail


connection = mail.get_connection()


class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def login(email: str = None, password: str = None):
        user_exist = User.objects.filter(email=email).exists()
        if user_exist:
            user_object = AuthService.check_email_existence(email)
            user = authenticate(email=user_object.email, password=password)
            if user:
            
                token = RefreshToken.for_user(user_object)
                refresh_token = str(token)
                access_token = str(token.access_token)

                
                login_response = {
                    "user_id":str(user_object.user_id),
                    "first_name":user_object.first_name,
                    "last_name":user_object.last_name,
                    "city":user_object.city,
                    "gender":user_object.gender,
                    "email": user_object.email,
                    "phone_number": user_object.phone_number,
                    "is_phone_verified": user_object.is_phone_verified,
                    "is_email_verified": user_object.is_email_verified,
                    "is_active": user_object.is_active,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return login_response
    

            else:
                raise PermissionDenied('Password Is Incorrect')
        else:
            raise PermissionDenied(f'Account With {email} Email Is Not Exist')
        

    @staticmethod
    def check_email_existence(email):
        try:
            user_object = User.objects.get(email=email)
        except ObjectDoesNotExist as oe:
            raise APIException("Email address not found in database")
        return user_object

    

    @staticmethod
    def check_login(self):
        try:
            if AuthService.login['token'] == RefreshToken.check_blacklist(self):
               return False
        except:
            return True

