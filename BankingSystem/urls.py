from django.contrib import admin
from django.urls import path,include
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home_page'),
    path('accounts/', include('users.urls')),
    path('', include('Bank.urls')),
]
