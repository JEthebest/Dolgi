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
    path(
        'agent_debts/', deb_views.agent_debts,
        name='agent_debts'
    ),
    path('my_debts/', deb_views.my_debts, name='my_debts'),
    path('debts_to_me/', deb_views.debts_to_me, name='debts_to_me'),
    path('create_agent/', deb_views.create_agent, name='create_agent'),
    path('create_debt/', deb_views.create_debt, name='create_debt'),
    path('update_debt/<int:pk>/', deb_views.update_debt, name='update_debt'),
    path('delete_debt/<int:pk>/', deb_views.delete_debt, name='delete_debt'),
    path(
        'account_statistics/', deb_views.account_statistics,
        name='account_statistics'
    ),
    path('agents_balance/', deb_views.agents_balance, name='agents_balance'),
    path('debts_history/', deb_views.debts_history, name='debts_history'),
    path('turnover/', deb_views.turnover, name='turnover'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users_url)),
    path('debt/', include(debts_url)),
]
