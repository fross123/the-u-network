from django import forms
from django_quill.forms import QuillFormField

class NewPost(forms.Form):
    content = QuillFormField()
