
from django.contrib import admin
from .models import Post, EditLogs #, Profile #Profile added

admin.site.register(Post)
admin.site.register(EditLogs)

#added
#admin.site.register(Profile)
#*************************************************************
'''
#NOPE
from .forms import SignUpForm

from django.contrib.auth.models import User



#admin.site.register(SignUpForm)

class MyModelAdmin(admin.ModelAdmin):
      form = SignUpForm

admin.site.register(User, MyModelAdmin)
'''
#*********************************************************************************

'''
#NOPE
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm
from django.contrib.auth.models import User

#from .forms import CustomUserChangeForm, CustomUserCreationForm
#from .models import CustomUser


class CustomUserAdmin(UserAdmin):
	#add_form = CustomUserCreationForm
	#form = CustomUserChangeForm
	form=SignUpForm
	#model = CustomUser
	model=User
	#list_display = ["email", "username", "age", "is_staff"]
	add_fieldsets = (
	    (
		None,
		{
		    "classes": ("wide",),
		    "fields": ("username", "name", "domain", "is_stakeholder", "password1", "password2"),
		},
	    ),
	)


admin.site.register(CustomUserAdmin)
'''
