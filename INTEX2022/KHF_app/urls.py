from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPageView, name='index'),
    path('viewDashboard/', views.viewDashboard, name='viewDashboard' ),
    path('viewAccount/', views.viewAccount, name='viewAccount'),
    path('fillAccount/', views.fillAccount, name='fillAccount'),
    path('logout/', views.logout, name='logout'),
    path('users', views.storeUserPageView, name='storeuser'),
    path('storeMealView', views.storeMealView, name='storemealView'),
]

