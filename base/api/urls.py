from django.urls import path
from . import views


urlpatterns =[

    path('', views.getRouts,name='api'),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]