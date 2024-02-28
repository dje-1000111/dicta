"""Urls dictation."""

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView
from apps.dictation.models import Dictation
from apps.dictation import views

app_name = "dictation"

info_dict = {
    "queryset": Dictation.objects.all(),
    "date_field": "change_date",
}

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("topic/<slug>/", views.TopicView.as_view(), name="topic"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "aptc/",
        views.AjaxDetailView.as_view(),
        name="ajax_post_textarea_content",
    ),
    path("aprr/", views.post_user_rating, name="ajax_post_request_rating"),
    path(
        "aprd/",
        views.post_request_definition,
        name="ajax_post_request_definition",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "BingSiteAuth.xml",
        TemplateView.as_view(
            template_name="BingSiteAuth.xml", content_type="text/xml; charset='utf-8'"
        ),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"dicta": GenericSitemap(info_dict, priority=0.8)}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
