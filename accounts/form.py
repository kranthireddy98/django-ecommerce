from typing import Any
from django import forms

from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
        'class' : 'form-control'
    }))
    class Meta:

        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
    
    def __init__(self, *args, **kwargs):
           super(RegistrationForm,self).__init__(*args, **kwargs)
           
           for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
                if field !='confirm_password':
                    self.fields[field].widget.attrs['placeholder'] = 'Enter' +' ' +  field.replace('_'," ").capitalize()
        
    def clean(self) -> dict[str, Any]:
         cleaned_data = super(RegistrationForm, self).clean()
         password = cleaned_data.get('password')
         confirm_password = cleaned_data.get('confirm_password')

         if password != confirm_password:
              raise forms.ValidationError(
                   'password does not match!'
              )
         

