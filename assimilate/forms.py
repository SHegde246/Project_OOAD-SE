from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post
#from .models import Profile #added

#from betterforms.multiform import MultiModelForm #added


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'domain', 'content',)
        
        #not seen, but are still attached with form
        exclude = ('user',)
 
 
        

#**********************************************************************************************
'''
#added
#version 2
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','domain', 'is_stakeholder')
        
        
class UserCreationMultiForm(MultiModelForm):
	form_classes = {
	'user': UserCreationForm,
	'profile': ProfileForm,
	}
    
	def save(self, commit=True):
		objects = super(UserCreationMultiForm, self).save(commit=False)

		if commit:
		    user = objects['user']
		    user.save()
		    profile = objects['profile']
		    profile.user = user
		    profile.save()

		return objects
        
	def clean(self):
		cd = self.cleaned_data

		password1 = cd.get("user-password1")
		password2 = cd.get("user-password2")

		if password1 != password2:
		#Or you might want to tie this validation to the password1 field
			raise ValidationError("Passwords did not match")
		

		return cd
'''
#**********************************************************************************************


        

'''
#NOPE

#version 1

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','domain', 'is_stakeholder')
'''



#extending the default user registration form
#default has username, password1, password2 (confirmation).
#we're adding name, is_stakeholder and domain
class SignUpForm(UserCreationForm):
	#user = models.OneToOneField(User, on_delete=models.CASCADE)	
	
	
	name = forms.CharField(max_length=30, required=True, help_text='Enter your account display name.')
	domain= forms.CharField(max_length=30, required=True, help_text='Enter the domain.')
	is_stakeholder=forms.BooleanField(required=False)
	
	class Meta:
		model=User
		fields=('username', 'name', 'domain', 'is_stakeholder', 'password1', 'password2')

