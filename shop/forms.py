from django import forms
from django.contrib.auth.models import User
from .models import Purchase


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'birthday']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.profile.birthday = self.cleaned_data['birthday']
            user.profile.save()
        return user


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["address"]
