from django.contrib import admin
from django.urls import path, include

from apps.users import views
from apps.debts import views as deb_views


users_url = [
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
    path('', deb_views.debts_list, name='debts_list'),
    path('agents/create/', deb_views.create_agent, name='create_agent'),
    path(
        'agents/<int:agent_id>/', deb_views.agent_detail,
        name='agent_detail'
    ),
    path(
        'agents/<int:agent_id>/take_loan/', deb_views.take_loan,
        name='take_loan'
    ),
    path(
        'agents/<int:agent_id>/give_loan/', deb_views.give_loan,
        name='give_loan'
    ),
    path('debts/<int:debt_id>/', deb_views.debt_detail, name='debt_detail'),
    path(
        'debts/<int:debt_id>/increase_loan/', deb_views.increase_loan,
        name='increase_loan'
    ),
    path('debts/<int:debt_id>/pay_debt/', deb_views.pay_debt, name='pay_debt'),
    path(
        'account/statistics/', deb_views.account_statistics,
        name='account_statistics'
    ),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users_url)),
    path('debt/', include(debts_url)),
]
