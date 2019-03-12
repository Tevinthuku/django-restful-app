from django import forms

from .models import Status
from cfeapi.utils import check_for_whitespaces


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            "id",
            "user",
            "content",
            "image"
        ]

    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        if len(content) > 240:
            raise forms.ValidationError("Content is too long")
        return content

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        check_for_whitespaces(data, ["content"])
        return super().clean(*args, **kwargs)
