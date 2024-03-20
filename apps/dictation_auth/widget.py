"""Custom widget."""

from django.conf import settings
from django_recaptcha.widgets import ReCaptchaBase


class CustomReCaptchaV3(ReCaptchaBase):
    input_type = "hidden"
    template_name = "registration/custom_widget_v3.html"

    def __init__(self, api_params=None, action=None, *args, **kwargs):
        super().__init__(api_params=api_params, *args, **kwargs)
        if not self.attrs.get("required_score", None):
            self.attrs["required_score"] = getattr(
                settings, "RECAPTCHA_REQUIRED_SCORE", None
            )
        self.action = action

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        return attrs

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update({"action": self.action})
        return context
