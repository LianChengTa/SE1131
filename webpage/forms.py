from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm,PasswordChangeForm
from .models import user_account, add_event


class loginform(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("賬號不能为空。")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("密碼不能为空。")
        return password



class registerform(UserCreationForm):
    first_name = forms.CharField(max_length=150, label="姓名")
    studentid = forms.CharField(max_length=20, label="學號")

    class Meta:
        model = user_account
        fields = ['username', 'first_name', 'studentid', 'password1', 'password2']


class profile_edit_form(UserChangeForm):
    first_name=forms.CharField(
        label='名稱'
    )
    password=None
    class Meta:
        model=user_account
        fields=['username','first_name','studentid']
        widgets={
            'username': forms.TextInput(attrs={'readonly':'readonly'})
        }
        help_texts = {
            'username': 'Username不能修改！',
        }

class password_edit_form(PasswordChangeForm):
    old_password = forms.CharField(
        label="舊密碼", 
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True})
    )
    new_password1 = forms.CharField(
        label="新密碼", 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    new_password2 = forms.CharField(
        label="確認新密碼", 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

class add_event_form(forms.ModelForm):
    class Meta:
        model = add_event
        fields = ['title', 'description', 'venue', 'event_date', 'registration_deadline']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    