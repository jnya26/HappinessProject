from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)


class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=30)
    team_logo = forms.URLField()
