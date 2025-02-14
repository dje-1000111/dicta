from django import forms
from apps.dictation.models import Dictation


class DictationForm(forms.Form):
    """Dictation form."""

    textarea = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100 p-2",
                "rows": 4,
                "placeholder": "Transcribe the sentences you hear...",
                "autofocus": True,
                "autocomplete": "off",
                "autocapitalize": "off",
                "spellcheck": "false",
                "data-gramm": "false",
                "data-gramm_editor": "false",
                "data-enable-grammarly": "false",
            }
        ),
    )

    def clean(self):
        """Clean."""
        cleaned_data = super().clean()
        data = cleaned_data.get("textarea")
        return data


class AutoDictationForm(forms.ModelForm):
    """Auto dictation form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["video_id"].required = True

    class Meta:
        """Meta."""

        model = Dictation
        fields = ["video_id"]
        labels = {"video_id": ""}
        widgets = {
            "video_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "id_video_id",
                    "placeholder": "Video ID",
                },
            )
        }
