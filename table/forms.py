from django import forms

comment = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Text!"}))
