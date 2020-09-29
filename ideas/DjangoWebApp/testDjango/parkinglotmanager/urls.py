from django.urls import path
from . import views

urlpatterns = [
    path('plm/',views.index, name='plm-index'), 
    path('plm/edit/', views.edit, name='plm-eidt')
]