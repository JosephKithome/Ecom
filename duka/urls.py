from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.register, name="register"),
    # path('login/', views.loginPage, name='login'),
    path('', views.duka, name="duka"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

]
