from django import forms

class TagWidget(forms.TextInput):
    template_name = 'django/forms/widgets/text.html'

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        attrs.setdefault('class', 'form-control')
        attrs.setdefault('placeholder', 'Enter tags separated by commas')
        kwargs["attrs"] = attrs
        super().__init__(*args, **kwargs)
