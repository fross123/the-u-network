from django import forms

class NewPost(forms.Form):
    content = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'content', 'rows': '4', 'placeholder': 'Say something...hilarious!'}), label="")
