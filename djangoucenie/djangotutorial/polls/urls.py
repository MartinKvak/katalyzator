from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/', views.rental_details, name='rental_details'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path("delete_user/", views.delete_user, name="delete_user"),
    path('my_reservations/', views.user_reservations, name='user_reservations'),
    path('cancel_reservation/<int:car_id>/', views.cancel_reservation, name='cancel_reservation'),
]
