from sales import views
from django.urls import path

urlpatterns = [
     path('', views.login_view, name='login'), # login page
     path('home/', views.home, name='home'), # home page
     path('submit/', views.submit, name='submit'), # 'thank you' page
     path('cart/', views.cart, name='cart'), # cart page
     path('update_count/<int:item_id>/', views.update_item_count, name='update_item_count'), #countupdate
     path('reset_count/<int:item_id>/', views.reset_count, name='reset_count'), #reset count 
     path('reset_all_counts/', views.reset_all_counts, name='reset_all_counts'), #resetAll 
     path('register/', views.register, name='register'), #register page
     path('logout/', views.logout_view, name='logout'), # log out button on navbar
     path('get_cart_count/', views.get_cart_count, name='get_cart_count'), # get cart count update for navbar
     path('get_cart_total/', views.get_cart_total, name='get_cart_total'), # get cart total updates
]