from django.contrib import admin
from django.urls import path, include

from apps.users import views
from apps.debts import views as deb_views


users_url = [
    path('home/', views.home, name='home'),
    path('', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path(
        'password_reset/',
        views.UserPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        views.UserPasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        views.UserPasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]


debts_url = [
    path('main/', deb_views.main_dolgi, name='main'),
    path(
        'borrow/', deb_views.borrow,
        name='borrow_money'
    ),
    path(
        'repay/<int:transaction_id>/<str:slug>/',
        deb_views.repay, name='repay'
    ),
    path('lend/', deb_views.lend, name='lend_money'),
    path(
        'receive_payment/<int:transaction_id>/',
        deb_views.receive_payment, name='receive_payment',
    ),
    path('my_debts/', deb_views.my_debts, name='my_debts'),
    path('debts_to_me/', deb_views.debts_to_me, name='debts_to_me'),
    path('contacts/<str:slug>/', deb_views.my_contacts, name='contacts'),
    path('create/contact/', deb_views.create_contact, name='create_contact'),
    path('take_loan/<str:slug>/', deb_views.take_loan, name='take_loan'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users_url)),
    path('debt/', include(debts_url)),
]
