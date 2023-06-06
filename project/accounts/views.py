from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SingUpForm

class SingUp(CreateView):
    model = User
    form_class = SingUpForm
    success_url = '/accounts/login'

    template_name = 'registration/register.html'
