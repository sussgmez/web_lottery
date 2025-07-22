from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from .forms import SignUpForm, LoginForm


class SignUpView(View):
    template_name = "authentication/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.signup(request)
            return redirect("login")
        else:
            return render(request, self.template_name, {"form": form})


class LoginView(TemplateView):
    template_name = "authentication/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})


def logout_handler(request):
    logout(request)
    return redirect("login")
