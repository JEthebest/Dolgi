from django.urls import path

from apps.users import views


users_url = [
    path('', views.unauthorized_menu, name='unauthorized_main'),
    path('login/', views.UserLoginView.as_view(), name='login'),
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
