"""Urls dictation."""

from django.urls import path
from django.views.generic import TemplateView
from apps.dictation import views

app_name = "dictation"

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
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="text/xml; charset='utf-8'"
        ),
    ),
]
