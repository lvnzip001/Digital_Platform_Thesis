from ast import Pass
from pyexpat import model
from django import forms
from .models import  Embed_Ownership_Text, Embed_Ownership_Image, Embed_Enforcement_Sound, Embed_Enforcement_Text, Embed_Enforcement_Image,Embed_Ownership_Sound,User_Info,Extract_Embedded_Text,Extract_Embedded_Sound,Extract_Embedded_Image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class UserForm(forms.ModelForm):
    class Meta:
        model = User_Info
        fields = '__all__'
        exclude = ['user']

class Embed_Ownership_Text_Form(forms.ModelForm):
    class Meta:
        model = Embed_Ownership_Text
        fields = '__all__'

class Embed_Ownership_Image_Form(forms.ModelForm):
    class Meta:
        model = Embed_Ownership_Image
        fields = '__all__'
        

class Embed_Ownership_Sound_Form(forms.ModelForm):
    class Meta:
        model = Embed_Ownership_Sound
        fields = '__all__'

class Embed_Enforcement_Text_Form(forms.ModelForm):
    class Meta:
        model = Embed_Enforcement_Text
        fields = '__all__'

class Embed_Enforcement_Image_Form(forms.ModelForm):
    class Meta:
        model = Embed_Enforcement_Image
        fields = '__all__'

class Embed_Enforcement_Sound_Form(forms.ModelForm):
    Pass
    class Meta:
        model = Embed_Enforcement_Sound
        fields = '__all__'

class Extract_Embedded_Sound_Form(forms.ModelForm):
    class Meta:
        model = Extract_Embedded_Sound
        fields = ('source_file','file')

class Extract_Embedded_Image_Form(forms.ModelForm):
    class Meta:
        model = Extract_Embedded_Image
        fields = ('source_file','file')

class Extract_Embedded_Text_Form(forms.ModelForm):
    class Meta:
        model = Extract_Embedded_Text
        fields = ('source_file','file')