from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.views.generic import ListView, DetailView, UpdateView, UpdateView
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import JsonResponse
import smtplib
from email.message import EmailMessage
from django.utils.translation import gettext_lazy as _
from .country import block_names



# LOGIN
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    alert = False
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate(username=username, password=password):
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, _('Password is incorrect!'))
                return redirect('login')
        if next:
            return redirect(next)

    
    context = {'form': form,'alert':alert, 'title': _("Log in")}
    return render(request, "registrations/login.html", context)

# Welcom Message   
def email_message(obj, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = obj
    msg['to'] = to
    username = 'hagmir7@gmail.com'
    msg['from'] = username
    password = 'jfpgqzkxetgyjbvo'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()




# REGISTER 
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = new_user.email
            new_user.save()
            return redirect('/admins')
    context = {'title': _('Register'), 'form': form, }
    return render(request, 'registrations/register.html', context)





class ProfileViewUpdate(UpdateView):
    model = Profile
    template_name = 'profile/update_profile.html'
    form_class = UpdateProfile
    success_url = reverse_lazy('home')
    success_message = _('Profile updated successfully!')

    def get_context_data(self, *arge, **kwargs):
        context = super(ProfileViewUpdate, self).get_context_data(
            *arge, **kwargs)
        page = get_object_or_404(Profile, id=self.kwargs['pk'])
        title = _('Update Profile')
        context["page"] = page
        context["title"] = title
        return context





    

def user_update_info(request):
    confirm = False
    if request.method == 'POST':
        form = UserUpdateInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            confirm = True
    else:
        form = UserUpdateInfo(instance=request.user)
    context = {'form': form, 'confirm':confirm, 'title': _("Contact information")}
    return render(request, 'profile/user_update_info.html', context)





class PasswordChange(PasswordChangeView):
    template_name = 'profile/change-password.html'
    success_url = reverse_lazy('home')

class PasswordChangeDone(ListView):
    
    template_name = 'profile/change-password-done.html'
    success_url = reverse_lazy('home')


def posword_reset_done(request):
    context = {'title':_("Password reset has been sent")}
    return render(request, 'password_reset/reset_password_done.html', context)


def deleteUser(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, 'Administrateur supprimé avec succès')
    return redirect('/admins')


        


