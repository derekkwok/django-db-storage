from django import forms

from dbstorage.models import DBFile


class DBFileForm(forms.ModelForm):

    file = forms.FileField()

    class Meta:
        model = DBFile
        fields = ['name']

    def save(self, commit=True):
        db_file = super(DBFileForm, self).save(commit=False)
        db_file.content = self.cleaned_data['file'].read()
        if commit:
            db_file.save()
        return db_file
