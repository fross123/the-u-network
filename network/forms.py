from django import forms

class NewPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'content', 'rows': '4'}), label="Content")
