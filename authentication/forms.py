from django import forms
from django.contrib.auth import authenticate, login
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class':'input', 'autofocus':''}), 
        max_length=150, 
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'input'}), 
        required=True
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
    
    def login(self, request):
        email = self.cleaned_data.get('email')
        user = CustomUser.objects.get(email=email)
        login(request, user)

  
class SignUpForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'singup-form__input'}), 
        max_length=100, 
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'singup-form__input'}), 
        max_length=100, 
        required=True
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type':'email', 'class':'singup-form__input'}), 
        required=True
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'signup-form__input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'signup-form__input'}))
    phone_number = forms.TextInput(attrs={'type':'number'})
    
    class Meta:
        model = CustomUser

    def clean(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError("Correo electrónico ya registrado.")
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden.")
        
    def signup(self, request):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 == password2:

            user = CustomUser.objects.create(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=request.POST['code']+request.POST['phone_number']
            )
            user.set_password(password1)
            user.save()

       

