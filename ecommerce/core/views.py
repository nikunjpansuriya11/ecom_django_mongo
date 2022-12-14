from django.shortcuts import  render, redirect
from .models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import random
import re
import requests
from django.conf import settings
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.views.decorators.csrf import csrf_exempt # import
from rest_framework_simplejwt.tokens import RefreshToken
from ecom_api.models import *
from ecom_api.services.cart_services import all_cart_product, cart_data_serializer
ssl._create_default_https_context = ssl._create_unverified_context


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

# funcation for get user tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# funcation for send otp on email to user
def send_otp_on_email(to_emails, email_subject, html_content):
	message = Mail(settings.EMAIL_HOST_USER,to_emails,email_subject,html_content)
	try:
		sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
		response = sg.send(message)
	except Exception as e:
		print(e)

# funcation for send otp on phone number to user
def send_otp_on_phone(phone_number, otp):
	try:
		url = f'https://2factor.in/API/V1/{settings.TWOFACTOR_API_KEY}/SMS/{phone_number}/{otp}'
		response = requests.get(url)

		return True
	except Exception as e:
		return False
		
# funcation for email validation
def email_validator(email):
    if email is not None:
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    else:
        return False


# funcation for password validation
def password_validator(password):
    if password is not None:
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        
        # compiling regex
        pat = re.compile(reg)
        
        # searching regex                 
        mat = re.search(pat, password)
        
        # validating conditions
        if mat:
            return True
        else:
            return False
    else:
        return False

# funcation for Phone nummber validation
def phone_number_validator(phone_number):
    reg = re.compile("((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}")
    mat = reg.match(phone_number)
    return mat
  

# funcation for user registertion and validation 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt 
def register_user(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
		if request.method == "POST":
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			city = request.POST['city']
			email = (request.POST['email']).lower()
			phone_number = request.POST['phone_number']
			gender = request.POST['gender']
			password = request.POST['pass']
			re_password = request.POST['re_pass']

			if first_name is not None and last_name is not None and email_validator(email) and phone_number_validator(phone_number) and gender is not None and password_validator(password) and re_password is not None and city is not None:
				if password == re_password:
					if not User.objects.filter(email=email.lower()).exists():
						if not User.objects.filter(phone_number=phone_number).exists():


							email_otp = random.randint(100000,999999)
							phone_otp = random.randint(100000,999999)

							email_body = "Your Verification Code is : " + str(
								email_otp
							)
							response = send_otp_on_email(
								email, "Verification OTP", email_body
							)

							send_otp_on_phone(phone_number, phone_otp)
					
							user_datas = User.objects.create_user(first_name=first_name,last_name=last_name,city=city,gender=gender,email=email,phone_number=phone_number,password=password,email_otp=email_otp,phone_otp=phone_otp)
							request.session['email'] = email
							messages.success(request, "Registration successful,now verification of email, phone number." )
							return redirect("verification")
						else:
							messages.error(request, "Phone Number Already Exists")
					else:
						messages.error(request, "Email Already Exists")
				else:
					messages.error(request, "Password didn't match")
			else:
				messages.error(request, "Please Enter Valid details.")
	return render(request, "signup.html")
                    
# funcation for verification of user 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validation_user(request):
	if 'email' in request.session:
		if request.method == "POST":
			if 'resend' in request.POST:
				user_data = User.objects.get(email=request.session['email'])
				email = request.session['email']
				email_otp = random.randint(100000,999999)
				phone_otp = random.randint(100000,999999)

				user_data.email_otp = email_otp
				user_data.phone_otp = phone_otp
				user_data.save()

				email_body = "Your Verification Code is : " + str(
					email_otp
				)
				response = send_otp_on_email(
				 email, "Verification OTP", email_body
				)

				send_otp_on_phone(user_data.phone_number, phone_otp)

			else:
				re_email_otp = request.POST['email_otpv']
				re_phone_otp = request.POST['phone_otpv']
				

				user_data = User.objects.get(email=request.session['email'])
				check_email_otp = user_data.email_otp
				check_phone_otp = user_data.phone_otp
				
				if check_email_otp == re_email_otp and re_phone_otp == check_phone_otp:
					user_data.is_phone_verified = True
					user_data.is_email_verified = True
					user_data.is_active = True
					user_data.save()
					user = User.objects.get(email=request.session['email'])
					return redirect('login')
		return render(request, "varification.html")
	return redirect('login')

# funcation for user login and validation of email, password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt  # add this token before defining function
def login_user(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
		if request.method == "POST":
			email = request.POST['email']
			password = request.POST['password']
			if User.objects.filter(email=email).exists():
				user_data = User.objects.get(email=email)
				password_db = user_data.password 
				checkuser=authenticate(email=email, password=password)
				if checkuser:

					if user_data.is_phone_verified == False or user_data.is_email_verified == False:
						email_otp = random.randint(100000,999999)
						phone_otp = random.randint(100000,999999)
						user_data.email_otp = email_otp
						user_data.phone_otp = phone_otp
						user_data.save()

						email_body = "Your Verification Code is : " + str(
							email_otp
						)
						response = send_otp_on_email(
						email, "Verification OTP", email_body
						)

						send_otp_on_phone(user_data.phone_number, phone_otp)
						request.session['email'] = email

						return redirect('verification')
					if user_data.is_active == False:
						messages.error(request, "User Deactive by admin.")
						return render(request, "signin.html")
				
					login(request, user_data)
					token_data = get_tokens_for_user(user_data)
					request.session['access_token'] = token_data['access']
					messages.info(request, f"You are now logged in as {email}.")
					return redirect("home")
				else:
					messages.error(request, "Enter valid Password.")
			else:
				messages.error(request, "User not found.")

	return render(request, "signin.html")


# funcation for user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

# funcation for home page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
	return render (request, "home.html", )

# funcation for products pages
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product(request):	
	if request.method == "POST":

		token_data = get_tokens_for_user(request.user)
		request.session['access_token'] = token_data['access']
		data_id = request.POST['id']

		host = request.META['HTTP_HOST']
		url = "http://"+host+"/api/cart/"

		payload={'product_id': data_id}
		files=[
		]
		headers = {
		'Authorization': 'Bearer '+ request.session['access_token']
		}
		response = requests.request("POST", url, headers=headers, data=payload, files=files)
		return redirect('product')

	path = str(request.path).replace("/","")
	type = ""
	
	if path == "new_arrivals":
		type = "new arrivels"
	elif path == "men":
		type = "mens"
	elif path == "women":
		type = "womens"
	elif path == "kids":
		type = "kids"
	elif path == "sport":
		type = "sport"
	elif path == "outlet":
		type = "outlet"


	search = request.GET.get('search')
	price_sort = request.GET.get('price_sort')
	name_sort = request.GET.get('name_sort')
	page = request.GET.get('page')
	per_page = 21	

	search = request.GET.get('search')
	price_sort = request.GET.get('price_sort')
	name_sort = request.GET.get('name_sort')
	page = request.GET.get('page')

	if search == None:
		search = ""
	if price_sort == None:
		price_sort = ""
	if name_sort == None:
		name_sort = ""
	if page == None:
		page = ""


	host = request.META['HTTP_HOST']
	url = "http://"+host+"/api/products/"
	params = {'search': search,
	'price_sort': price_sort,
	'name_sort': name_sort,
	'type':type,
	'page': page}

	payload={}
	headers = {}

	response = requests.request("GET", url, params=params,headers=headers, data=payload)
	product_data = response.json()

	page_list = []
	for i in range(1,int(product_data['last_page'])+1):
		page_list.append(i)


	return render(request, "product.html", { "product_data" : product_data['data'], "current_page_number":int(product_data['current_page']), "last_page":int(product_data['last_page']), "page_list":page_list } )

# funcation for cart page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def cart(request):	
	if request.method == "POST":

		token_data = get_tokens_for_user(request.user)
		request.session['access_token'] = token_data['access']
		data_id = request.POST['id']

		host = request.META['HTTP_HOST']
		url = "http://"+host+"/api/cart/"

		payload={'product_id': data_id}
		files=[
		]
		headers = {
		'Authorization': 'Bearer '+ request.session['access_token']
		}

		response = requests.request("DELETE", url, headers=headers, data=payload, files=files)
		return redirect('cart')
	product_object = all_cart_product(request.user.user_id)
	if product_object:
		serialized_response = cart_data_serializer(product_object)	
		product_data = serialized_response['Products']
	else:
		product_data = None

	return render(request, "cart.html", { "product_data" : product_data  } )


