from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """
    This class generates the form for the user registration form.
    It is used by the templates:
        -register.html
        -onboard_employee.html
   It is displayed on pages:
        - /register

    The fields for registration are: username, email, password and password confirmaton.
    """

    acceptable_emails = ['nhs.net', 'nhs.co.uk', 'ac.uk', 'googlemail.com', 'gmail.com', "abv.bg","stepchange.com"]

    def clean_email(self):
        nhs_email_test = self.cleaned_data['email'].split('@')[-1]
        academic_email_test = self.cleaned_data['email'][-5:]
        if nhs_email_test not in self.acceptable_emails and academic_email_test not in self.acceptable_emails:
            raise forms.ValidationError(
                f"Email address not allowed. Please use an '@nhs.net', '@nhs.co.uk' or '.ac.uk' email address.")
        return self.cleaned_data['email']

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    This class generates the form for the user profile update form.
    It is used by the templates:
        -profile.html
    It is displayed on pages:
        - /profile
    The fields for update are: username and email.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class CreateModerator(UserCreationForm):
    acceptable_emails = ['nhs.net', 'nhs.co.uk', 'ac.uk',"gmail.com","abv.bg","stepchange.com"]

    def clean_email(self):
        nhs_email_test = self.cleaned_data['email'].split('@')[-1]
        academic_email_test = self.cleaned_data['email'][-5:]
        if nhs_email_test not in self.acceptable_emails and academic_email_test not in self.acceptable_emails:
            raise forms.ValidationError(
                f"Email address not allowed. Please use an '@nhs.net', '@nhs.co.uk' or '.ac.uk' email address.")
        return self.cleaned_data['email']

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
