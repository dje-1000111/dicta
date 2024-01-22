"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.urls import path, include

app_name = "youdictube"
handler404 = "apps.dictation.views.error_404"

admin.site.site_title = "dictatube site admin (DEV)"
admin.site.site_header = mark_safe(
    "dictatube administration -> Run the management/command <span style='color: red;'>update_total_line</span> after adding a new dictation"
)
admin.site.index_title = "Site administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.dictation_auth.urls")),
    path("", include("apps.dictation.urls")),
]