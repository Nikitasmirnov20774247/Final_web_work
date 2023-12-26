from django.contrib.auth.models import User
from django import forms


class RegUserForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(min_length=8, required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(RegUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if User.objects.filter(email=cleaned_data.get("email")):
            raise forms.ValidationError("Указанная почта уже используется")

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
