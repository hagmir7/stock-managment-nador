from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')

    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #         if not user:
    #             raise forms.ValidationError(_('The password or username is incorrect'))
    #         if not user.check_password(password):
    #             raise forms.ValidationError(_('Password is incorrect'))

    #     return super(UserLoginForm, self).clean(*args, **kwargs)
    
    def clean_username(self):
        cd = self.cleaned_data
        if not User.objects.filter(username=cd['username']).exists():
            raise ValidationError(_('There is no registered user with this name!'))
        return cd['username']

 



            

        



        

        


class SignUpForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')



class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), max_length=30,help_text=_(
        "Le nom d'utilisateur ne doit pas contenir d'espaces"),
         widget=forms.TextInput(attrs={
             'class': 'form-control input-size bg-secondary',
              'placeholder': _("Nom d'utilisateur")}))
    username = forms.CharField(label=_("Nom d'utilisateur"), max_length=30,help_text=_("Le nom d'utilisateur ne doit pas contenir d'espaces"), widget=forms.TextInput(
        attrs={'class': 'form-control input-size', 'placeholder': _("Nom d'utilisateur")}))
    email = forms.EmailField(label=_('E-mail'), widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': _('E-mail')}))
    first_name = forms.CharField(label=_('Pr??nom'), widget=forms.TextInput(
        attrs={'class': 'form-control input-size', 'placeholder': _('Pr??nom')}))
    last_name = forms.CharField(label=_('Nom'),widget=forms.TextInput(
        attrs={'class': 'form-control input-size ', 'placeholder': _('Nom')}))
    password1 = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput(
        attrs={'class': 'form-control input-size', 'placeholder': _('Mot de passe')}), min_length=8)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control input-size', 'placeholder': _('Confirm Mot de passe')}), min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError(_('Le mot de passe ne correspond pas.'))
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise ValidationError(_('Il y a un utilisateur enregistr?? avec ce nom??!'))
        return cd['username']



    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise ValidationError(_('Il y a un utilisateur enregistr?? avec ce email!'))
        return cd['email']    




class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'cover', 'phone',
                  'gander', 'country', 'bio', 'birth' )
        widgets = {
            'gander': forms.Select(attrs={'class': 'form-control input-update'} ),
            'country': forms.Select(attrs={'class': 'form-control input-update'} ),
        }


class UserUpdateInfo(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    

class PasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def clean(self):
        cleaned_data = super(PasswordChange, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('The two passwords did not match'))
        return cleaned_data



