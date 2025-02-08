from tempfile import template

from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from schooldata.views import HomepageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/',HomepageView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='schooldata/forms/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
    path('data/', include('schooldata.urls')),
]
