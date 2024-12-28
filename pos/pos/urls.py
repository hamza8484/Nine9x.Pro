from django.urls import path,include
from pos.pos import views
from django.urls import path



urlpatterns = [
    path('pos/',views.pos_index,name="pos"),
]
