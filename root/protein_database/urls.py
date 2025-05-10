
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('protein_design.urls')), #add all urls from protein_design app
    
    path("__reload__/", include("django_browser_reload.urls")), #add django_browser_reload urls
]


