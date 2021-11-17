from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class CustomUserCreationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(required=True)
        self.fields['avatar'] = forms.ImageField(required=False)

    def save(self, request):
        user = super().save(request)
        avatar = self.cleaned_data.pop('avatar')
        login = self.cleaned_data.pop('login')
        user.login = login
        if avatar:
            user.avatar = avatar
        user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'login', 'avatar', )


