from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from dbstorage.models import DBFile

widget_template = """\
<table>
    <tbody>
        <tr>
            <td>Current File</td>
            <td><a href="{url}" target="_blank">{name}</a></td>
        </tr>
        <tr class="alt">
            <td style="vertical-align: middle">Replace File</td>
            <td>{input}</td>
        </tr>
    </tbody>
</table>
"""


class DBFileWidget(forms.FileInput):

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super(DBFileWidget, self).render(name, value, attrs, renderer)
        if not self.instance:
            return input_html

        context = {
            'input': input_html,
            'name': self.instance.name,
            'url': reverse('db_file', args=[self.instance.name]),
        }
        return mark_safe(widget_template.format(**context))


class DBFileForm(forms.ModelForm):

    file = forms.FileField(widget=DBFileWidget())

    class Meta:
        model = DBFile
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(DBFileForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        field = self.fields['file']
        field.widget.instance = instance
        if instance:
            field.required = False

    def save(self, commit=True):
        db_file = super(DBFileForm, self).save(commit=False)
        file = self.cleaned_data.get('file')
        if file:
            db_file.content = file.read()
        if commit:
            db_file.save()
        return db_file
