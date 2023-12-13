from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User


# Override allauth signup form to include names for customer model
class MyCustomSignupForm(SignupForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)

    def save(self, request):
        first_name = self.cleaned_data.pop('first_name')
        last_name = self.cleaned_data.pop('last_name')
        user = super(MyCustomSignupForm, self).save(request)
        return user