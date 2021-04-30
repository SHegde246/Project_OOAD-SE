from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


#from django.db.models.signals import post_save
#from django.dispatch import receiver

class Post(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    #domain = models.CharField(max_length=200, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
        
#model which holds all edited article objects
class EditLogs(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	old_title = models.CharField(max_length=200)
	new_title = models.CharField(max_length=200)
        
	old_content = models.TextField()
	new_content = models.TextField()
        
	edited_date = models.DateTimeField(blank=True, null=True)
        
	def __str__(self):
		return str(self.edited_date)
		
#for search
#will be overriding the field in the SearchForm class, which inherits from this
class Search(models.Model):
	search = models.CharField(max_length=30, help_text="search for articles based on title/content", default=" ")
	
	def __str__(self):
		return str(self.search)
        
#********************************************************************
'''
#added
#version 2
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
    	
	name = models.CharField(max_length=30, help_text='Enter your account display name.')
	domain= models.CharField(max_length=30, help_text='Enter the domain.')
	is_stakeholder=models.BooleanField()
	
	def __str__(self):
        	return str(self.user)
'''
  
        
        
#********************************************************************

'''
#NOPE

#version 1


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
    	
	name = models.CharField(max_length=30)
	domain= models.CharField(max_length=30)
	is_stakeholder=models.BooleanField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
'''       

'''      
#browse through articles with/without account        
class Browse(models.Model):
	title=models.TextField()
	author=models.TextField()
	domain=models.TextField()
	content=models.TextField()
	
	def __str__(self):
		return self.title
'''		
		

	
		
		
