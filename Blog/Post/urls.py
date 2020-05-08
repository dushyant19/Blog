from django.urls import path
from . import views

app_name='Post'

urlpatterns=[ 
    path('',views.listing,name='list'),
    path('create/',views.Create,name='create'),
    path('<slug:slug>/',views.Retrieve,name='retrieve'),
    path('<slug:slug>/edit/',views.Update,name='update'),
    path('<slug:slug>/delete/',views.Delete,name='delete'),
]