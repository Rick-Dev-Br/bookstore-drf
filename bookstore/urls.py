from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from books.views import index


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
    path("api/", include("books.urls")),
]
