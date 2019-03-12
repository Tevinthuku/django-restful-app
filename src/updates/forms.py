from django import forms

from .models import Update as UpdateModel
from cfeapi.utils import check_for_whitespaces


class UpdateModelForm(forms.ModelForm):
    class Meta:
        model = UpdateModel
        fields = [
            "user",
            "content",
            "image"
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        check_for_whitespaces(data, ["content"])
        return super().clean(*args, **kwargs)
