from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import LoginView, UserCreateView, UserSendVerificationView, UserVerificationView, ProductList, CartList

urlpatterns = [
    path('login/', csrf_exempt(LoginView.as_view()),name='user_login'),
    path('register/', csrf_exempt(UserCreateView.as_view())),
    path('sendveririfaction/', csrf_exempt(UserSendVerificationView.as_view())),
    path('veririfaction/', csrf_exempt(UserVerificationView.as_view())),
    path('products/', csrf_exempt(ProductList.as_view())),
    path('cart/', csrf_exempt(CartList.as_view())),
    
]