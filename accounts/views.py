from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login = form.cleaned_data.get('login')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,
                                    request.FILES or None,
                                    instance=request.user)
        messages.debug(request, f'{request.POST}')
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('settings')

    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'registration/settings.html', context)
