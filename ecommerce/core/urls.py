from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("verification/", views.validation_user, name="verification"),
    path("login/", views.login_user, name="login"),
    path("product/", views.product, name="product"),
    path("new_arrivals/", views.product, name="new_arrivals"),
    path("men/", views.product, name="men"),
    path("women/", views.product, name="women"),
    path("kids/", views.product, name="kids"),
    path("sport/", views.product, name="sport"),
    path("outlet/", views.product, name="outlet"),
    path("cart/", views.cart, name="cart"),
    path("logout/", views.logout_user, name= "logout"),
    
]