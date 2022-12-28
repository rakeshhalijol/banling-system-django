from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name = 'index'),
    path('index',views.index,name = 'index'),
    path('login/',views.login,name = 'login'),
    path('login/login',views.login,name = 'login'),
    path('login/transactions/<int:id>',views.transactions,name = 'transactions'),
    path('login/delete/<int:id>/',views.delete,name = 'delete'),
    # path('login/notifications/',views.notifications,name = 'notifications')
    path('login/forgot/',views.forgot,name = 'forgot'),
    path('login/forgot/detials',views.forgot,name = 'forgot'),
    path('login/forgot/email_verified/<str:name>',views.email_verified,name = 'email_verifies')
]