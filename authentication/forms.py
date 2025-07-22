from django import forms
from django.contrib.auth import authenticate, login
from phonenumber_field.formfields import PhoneNumberField, SplitPhoneNumberField
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "input", "placeholder":"Correo electrónico", "autofocus": ""}),
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder":"Contraseña"}), required=True
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")

    def login(self, request):
        email = self.cleaned_data.get("email")
        user = CustomUser.objects.get(email=email)
        login(request, user)


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input", "placeholder":"Nombre"}),
        max_length=100,
        required=True,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input", "placeholder":"Apellido"}),
        max_length=100,
        required=True,
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "email", "class": "input", "placeholder":"Correo electrónico"}),
        required=True,
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input", "placeholder":"Contraseña"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input", "placeholder":"Confirmar contraseña"}))
    phone_number = SplitPhoneNumberField()

    class Meta:
        model = CustomUser

    def clean(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError("Correo electrónico ya registrado.")

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden.")

    def signup(self, request):
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 == password2:

            user = CustomUser.objects.create(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=request.POST["phone_number_0"]
                + request.POST["phone_number_1"],
            )
            user.set_password(password1)
            user.save()
