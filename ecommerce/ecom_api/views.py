import json
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.exceptions import APIException
from .serializers.login_serializer import LoginRequestSerializer, LoginResponseSerializer
from .services.auth_services import AuthService
from core.models import User
from .services.accounts_services import check_email_existence
from .services.product_serivces import get_all_product
from .services.cart_services import all_cart_product, cart_data_serializer
from .serializers.accounts_serializer import UserSerializer, UserResponseSerializer
from .serializers.product_serializer import AllProductSerializer
from .serializers.cart_serializer import CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
import random
from core.views import *
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from .models import Cart
import math


# class for login api
class LoginView(View):
    def post(self, request):
        try:    
            body_data = {
                        'email': request.POST['email'],
                        'password': request.POST['password'],
                    }
            if not User.objects.filter(email=request.POST['email'], is_phone_verified = False, is_email_verified=False).exists():
                serialized_request = LoginRequestSerializer(data=body_data, many=False)
                if serialized_request.is_valid():
                    login_response = AuthService.login(email=serialized_request.data.get('email'), password=serialized_request.data.get('password'))
                    serialized_response = LoginResponseSerializer(data=login_response, many=False)
                    if serialized_response.is_valid(raise_exception=True):
                        status = True
                        data = serialized_response.data
                        status_code = HTTP_200_OK
                        message = 'User Login Successfully.'
                        errors = {}
                    else:
                        data = {}
                        status = False
                        status_code = HTTP_401_UNAUTHORIZED
                        message = 'Email or Password Is Required.'
                        errors = {}
                else:
                    data = {}
                    status = False
                    status_code = HTTP_400_BAD_REQUEST
                    message = 'Email or Password Is Required.'
                    errors = serialized_request.errors
            else:
                data = {}
                status = False
                status_code = HTTP_401_UNAUTHORIZED
                message = 'First verify your account'
                errors = {}
                
        except APIException as ae:
            data = {}
            status_code = ae.status_code
            status = False
            message = 'Login failure'
            errors = ae.detail
        return JsonResponse({'status': status, 'data': data, 'message': message, 'status_code': status_code, 'errors': errors}, safe=False, status=status_code)


# class for user cretion api
class UserCreateView(View):
    def post(self, request):
        try:
            body_unicode = json.dumps(request.POST)
            body_data = json.loads(body_unicode)
            password = body_data['password']
            repassword = body_data['repassword']

            del body_data['repassword']
            if password_validator(password) and repassword is not None :
                if password == repassword:
                    serialized_request = UserSerializer(data = body_data, many=False)

                    if serialized_request.is_valid():
                        check_mail = check_email_existence(email=serialized_request.data.get('email'))
                        if check_mail is not None:

                            email_otp = random.randint(100000,999999)
                            phone_otp = random.randint(100000,999999)

                            email_body = "Your Verification Code is : " + str(
                                email_otp
                            )
                            response = send_otp_on_email(
                                serialized_request.data.get('email'), "Verification OTP", email_body
                            )
                            send_otp_on_phone(serialized_request.data.get('phone_number'), phone_otp)
                            
                            body_data['email_otp'] = email_otp
                            body_data['phone_otp'] = phone_otp

                            first_name = body_data['first_name']
                            last_name = body_data['last_name']
                            city = body_data['city']
                            email = (body_data['email']).lower()
                            phone_number = body_data['phone_number']
                            gender = body_data['gender']
                            password = body_data['password']

                            user = User.objects.create_user(first_name=first_name,last_name=last_name,city=city,gender=gender,email=email,phone_number=phone_number,password=password,email_otp=email_otp,phone_otp=phone_otp)

                            serialized_response = UserResponseSerializer(user, many=False)
                            if serialized_response.data:
                                data = serialized_response.data
                                status = True
                                status_code = HTTP_200_OK
                                message = f"User Registered Successfully"
                                errors = {}
                            else:                               
                                data = {}
                                status = False
                                status_code = HTTP_400_BAD_REQUEST
                                errors = {}
                        else:
                            data = {}
                            message = ""
                            status = False
                            status_code = HTTP_400_BAD_REQUEST
                            errors = 'email already exists'
                    else:
                        errors = serialized_request.errors
                        data = {}
                        message = ""
                        status = False
                        status_code = HTTP_400_BAD_REQUEST
                else:
                    data = {}
                    message = ""
                    status = False
                    status_code = HTTP_400_BAD_REQUEST
                    errors = 'Both password should be same'
            else:
                data = {}
                message = ""
                status = False
                status_code = HTTP_400_BAD_REQUEST
                errors = 'Enter Valid password and A password should be alphanumeric. password should be capital, Password must contain a special character (@, $, !, &, etc), Password length must be greater than 8 characters, One of the most important that the password fields should not be empty.'
        except APIException:
            data = {}
            status = False
            message = ""
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            errors = {}
        return JsonResponse({'status':status, "message":message, 'data':data, 'status_code': status_code, 'errors':errors})

# Class for user send otp for verification
class UserSendVerificationView(View):
    def post(self, request):  
 
        try:
            if User.objects.filter(email=request.POST['email']).exists():
                user_check = User.objects.filter(email=request.POST['email'], is_phone_verified=False, is_email_verified=False)
                if user_check   :
                    user_object = User.objects.get(email=request.POST['email'])
                    email_otp = random.randint(100000,999999)
                    phone_otp = random.randint(100000,999999)

                    email_body = "Your Verification Code is : " + str(
                        email_otp
                    )
                    response = send_otp_on_email(
                        user_object.email, "Verification OTP", email_body
                    )
                    send_otp_on_phone(user_object.phone_number, phone_otp)

                    user_object.email_otp = email_otp
                    user_object.phone_otp = phone_otp
                    user_object.save()

                
                    data = {"message":"Sucessfully send Otp"}
                    status = True
                    status_code = HTTP_200_OK
                else:
                    data = {}
                    status = "already verified"
                    status_code = HTTP_400_BAD_REQUEST
            else:
                data = {}
                status = "user "+ request.POST['email'] + "is not register"
                status_code = HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:  
            data = {}
            status = False
            status_code = HTTP_404_NOT_FOUND

        except Exception:
            data = {}
            status = False
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return JsonResponse({'status': status, 'data': data, 'status_code': status_code})   

# Class for user verification
class UserVerificationView(View):
    def post(self, request):  

        if User.objects.filter(email=request.POST['email']):
            user_object = User.objects.get(email=request.POST['email'])
            if user_object:
                re_email_otp = request.POST['email_otp']
                re_phone_otp = request.POST['phone_otp']
				

                check_email_otp = user_object.email_otp
                check_phone_otp = user_object.phone_otp
				
                if check_email_otp == re_email_otp and re_phone_otp == check_phone_otp:
                    user_object.is_phone_verified = True
                    user_object.is_email_verified = True
                    user_object.is_active = True
                    user_object.save()

            
                    data = {"message":"Sucessfully verified Otp"}
                    status = True
                    status_code = HTTP_200_OK
                else:
                    data = {"message":"Enter valid Otp"}
                    status = False
                    status_code = HTTP_400_BAD_REQUEST
            else:
                data = {}
                status = False
                status_code = HTTP_400_BAD_REQUEST
        else:
            data = {}
            status = "user "+ request.user.email + "is not register"
            status_code = HTTP_400_BAD_REQUEST
        
        return JsonResponse({'status': status, 'data': data, 'status_code': status_code})  

# Class for product api
class ProductList(APIView):
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get(self, request):
        search = request.GET.get('search')
        price_sort = request.GET.get('price_sort')
        name_sort = request.GET.get('name_sort')
        page = request.GET.get('page')
        type = request.GET.get('type')
        per_page = 21

        product_object = get_all_product()
        
        if len(product_object) > 0:

            if type:
                product_object = product_object.filter(type=type)

            if search:
                product_object = product_object.filter(Q(name__icontains=search) | Q(price__icontains=search) | Q(color__icontains=search))

            if price_sort == "asc":
                product_object = product_object.order_by('price')
            elif price_sort == "desc":
                product_object = product_object.order_by('-price')
            elif name_sort == "asc":
                product_object = product_object.order_by('name')
            elif name_sort == "desc":
                product_object = product_object.order_by('-name')
            
            if page:
                page = int(page)
            else:
                page = 1

            total = product_object.count()
            start = (page-1)*per_page
            end = page*per_page
            last_page = math.ceil(total/per_page)

            if page <= last_page:
                

                if product_object:
                    serialized_response = AllProductSerializer(product_object[start:end],many=True)
                    
                    data = serialized_response.data
                    response_message = "Success"
                    http_code = HTTP_200_OK
                    total_product = total
                    current_page = page
                    last_page = last_page
                else:
                    data = {}
                    response_message = "Product are not available"
                    http_code = HTTP_404_NOT_FOUND
                    total_product = 0
                    current_page = 0
                    last_page = 0
            else:
                data = {}
                response_message = "Page not available"
                http_code = HTTP_404_NOT_FOUND
                total_product = total
                current_page = 0
                last_page = last_page
        else:
            data = {}
            response_message = "Product are not available"
            http_code = HTTP_404_NOT_FOUND
            total_product = 0
            current_page = 0
            last_page = 0
           
    
        return JsonResponse({"message": {"message": response_message, "status": http_code}, 'data': data, 'total_product':total_product, 'current_page':current_page, 'last_page':last_page})



# Class for cart api
class CartList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        product_object = all_cart_product(request.user.user_id)
        if product_object:
            serialized_response = cart_data_serializer(product_object)
            
            data = serialized_response
            response_message = "Success"
            http_code = HTTP_200_OK
        else:
            data = {}
            response_message = "in Cart Product are not available"
            http_code = HTTP_404_NOT_FOUND
        
    
        return JsonResponse({"message": {"message": response_message, "status": http_code}, 'data': data})

    def post(self, request):   
        data = {
            "product_id":request.POST['product_id'],
        }

        if CartSerializer.validate_product(self, data=data):
            body_data = {
                "user_id":User.objects.get(user_id=request.user.user_id),
                "product_id":Product.objects.get(product_id=request.POST['product_id'])
            }

            cart_data = CartSerializer.create(self, validated_data=body_data)
            allcart_data = Cart.objects.get(user=request.user.user_id)
            serialized_response = cart_data_serializer(allcart_data)

            print(serialized_response)
            if serialized_response:
                data = serialized_response
                status = True
                status_code = HTTP_200_OK
                message = f"Product Add Successfully"
                errors = {}
            else:                               
                data = {}
                status = False
                status_code = HTTP_400_BAD_REQUEST
                message = f"ERROR"
                errors = {}
        else:
            print("aa")
            errors = "data not Valid"
            data = {}
            message = ""
            status = False
            status_code = HTTP_400_BAD_REQUEST
        
    
        return JsonResponse({'status':status, "message":message, 'data':data, 'status_code': status_code, 'errors':errors})

    def delete(self, request):   

        data = {
            "product_id":request.POST['product_id'],
        }
        if CartSerializer.validate_product(self, data=data):
            body_data = {
                "user_id":User.objects.get(user_id=request.user.user_id),
                "product_id":Product.objects.get(product_id=request.POST['product_id'])
            }

            cart_data = CartSerializer.delete(self, validated_data=body_data)
            allcart_data = Cart.objects.get(user=request.user.user_id)
            serialized_response = cart_data_serializer(allcart_data)

            if serialized_response:
                data = serialized_response
                status = True
                status_code = HTTP_200_OK
                message = f"Product Add Successfully"
                errors = {}
            else:                               
                data = {}
                status = False
                status_code = HTTP_400_BAD_REQUEST
                message = f"ERROR"
                errors = {}
        else:
            print("aa")
            errors = "data not Valid"
            data = {}
            message = ""
            status = False
            status_code = HTTP_400_BAD_REQUEST
        
    
        return JsonResponse({'status':status, "message":message, 'data':data, 'status_code': status_code, 'errors':errors})