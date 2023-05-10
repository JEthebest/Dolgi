from django.contrib import admin
from django.urls import path, include

from apps.users import urls
from apps.debts import urls as url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls.users_url)),
    path('debts/', include(url.debts_url)),
]
