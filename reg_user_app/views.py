from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
import logging


logger = logging.getLogger(__name__)

def reg(request):
    form = forms.RegUserForm()
    if request.method == 'POST':
        form = forms.RegUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            logger.info('User created')
            new_user = auth.authenticate(username=username, password=password)
            if new_user is not None:
                auth.login(request, new_user)
                return HttpResponseRedirect("/")           
    context = {
        'form': form,
    }
    return render(request, 'registration/reg.html', context=context)
