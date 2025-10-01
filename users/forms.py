from django import forms

from users.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=30,
        widget=forms.TextInput(attrs={
            'class' : 'login-form form-control',
            'placeholder' : '아이디 입력'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class' : 'password-form form-control',
            'placeholder' : '비밀번호 입력'}))

class SignupForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=15)
    password1 = forms.CharField(label="비밀번호" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 재입력", widget=forms.PasswordInput)
#
# class RevisionForm(forms.Form):
#     first_name = forms.CharField(min_length=3, max_length=15)
#     last_name = forms.CharField(min_length=3, max_length=15)
#     email = forms.EmailField(required=False)
#     profile_image = forms.ImageField(required=False)

class RevisionForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3)
    last_name = forms.CharField(min_length=3)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile_image"]
