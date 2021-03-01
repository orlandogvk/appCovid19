from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ModelSearch, ModelCodeSearch, ModelDateCode

#Form register users
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


#Form search results by date
class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.ModelForm):
    class Meta:
        model = ModelSearch
        fields = "__all__"
        widgets = {
            'date_input':DateInput()
        }


#Form search results by code
class TextInput(forms.TextInput):
    input_type = 'text'

class CodeForm(forms.ModelForm):
    class Meta:
        model = ModelCodeSearch
        fields = "__all__"
        widgets = {
            'code':TextInput()
        }



#Form search results by cod and date
class TextInputCountry(forms.TextInput):
    codeIn = 'text'
class DateInputCountry(forms.DateInput):
    dateIn = 'date'

class DateCodeForm(forms.ModelForm):
    class Meta:
        model = ModelDateCode
        fields = "__all__"
        widgets = {
            'date':DateInputCountry(),
            'code':TextInputCountry()
        }

 



