from django.urls import path

from apps.debts import views


debts_url = [
    path('', views.main_dolgi, name='main'),
    path('my_debts/', views.my_debts, name='my_debts'),
    path('debts_to_me/', views.debts_to_me, name='debts_to_me'),
    path(
        'transaction/contact/<str:transaction_type>/',
        views.transaction_contact,
        name='transaction_contact'
    ),
    path(
        'transaction/<str:transaction_type>/',
        views.transaction,
        name='transaction'
    ),
    path('contact/new/', views.new_contact, name='new_contact'),
]
