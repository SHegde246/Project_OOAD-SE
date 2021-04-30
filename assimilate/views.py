from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Post
from .forms import PostForm

from .forms import SignUpForm
#from .forms import UserForm
#from .forms import ProfileForm


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required



from django.contrib.auth.models import User


from django.contrib import messages

from .models import EditLogs

'''
#added
from django.views.generic import CreateView
from .forms import UserCreationMultiForm
from django.urls import reverse_lazy
#from django.core.urlresolvers import reverse_lazy
'''



def post_list(request):
	print(request.user)
	user_articles=Post.objects.filter(user=request.user).order_by('title')
	#user_articles = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'assimilate/post_list.html', {'articles': user_articles})
	
	#return render(request, 'assimilate/post_list.html', {'posts': user_articles})
    
   
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #print(str(post.user))
    #print(str(request.user))
    post_user=str(post.user)          #user (author) of the post
    loggedin_user=str(request.user)   #current logged-in user
    #print(type(post_user)==type(loggedin_user))
    #print(request.META['HTTP_REFERER'])
    #print(type(request.META['HTTP_REFERER']))
    
    #form = request.session.get('form')
    #print(form)
    #print(request.user.domain)
    
    return render(request, 'assimilate/post_detail.html', {'post': post, 'post_user': post_user, 'loggedin_user': loggedin_user})    
    #return render(request, 'assimilate/post_detail.html', {'post': post, 'post_user': post_user, 'loggedin_user': loggedin_user, 'reg_form': form})    

@login_required(login_url='login')     
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Article saved!!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'assimilate/post_edit.html', {'form': form})
 
''' 
#original  
@login_required(login_url='login')     
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'assimilate/post_edit.html', {'form': form})
'''   
    
'''    
#timestamp modification    
@login_required(login_url='login')     
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(post.title)
    print(post.content)
    title_old=post.title
    content_old=post.content
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            #only if change in content, update the timestamp
            if post.title!=title_old or post.content!=content_old:
            	post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'assimilate/post_edit.html', {'form': form})
'''    
    
    
#with edit_logs
@login_required(login_url='login')     
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(post.title)
    print(post.content)
    title_old=post.title
    content_old=post.content
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            
            #only if change in content, update the timestamp, and create new EditLogs object
            #it's being modified
            if post.title!=title_old or post.content!=content_old:
            	post.published_date = timezone.now()
            	EditLogs.objects.create(user=request.user, old_title=title_old, new_title=post.title, old_content=content_old, new_content=post.content, edited_date=post.published_date)
            	edit = EditLogs.objects.get(edited_date=post.published_date)
            	print(edit.user, edit.old_title, edit.new_title, edit.old_content, edit.new_content, edit.edited_date, sep="|")
            	
            	messages.success(request, 'Changes saved!!')
            	
            post.save()
            
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'assimilate/post_edit.html', {'form': form})
    
    
  
#original  
def register(request):
	if request.method=="POST":
		form=SignUpForm(request.POST)
		print(form.errors)
		if form.is_valid():
			new_user=form.save()
			print(request.user)
			
			#create a new session for new user
			#this is to pass the user info around across views (therefore, templates)
			request.session['form']=request.POST 
			
			#keep the user signed in after signing up
			new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
			login(request, new_user)
			print(request.user)
			
			return redirect("registered")      
			
			#form=User.objects.filter(user=request.user)
			#form=User.objects.get(pk=request.user.pk)
			#return redirect("registered",{'form':form})
			
		else:
			messages.error(request, 'Oops. Something went wrong. Enter valid details!') 
			return redirect("register")
	else:
		form=SignUpForm(request.POST)	
		#return render(request,"assimilate/register.html",{"form":UserCreationForm()})  
	return render(request, 'assimilate/register.html', {'form': form}) 
	

'''
#version 2	
class register(CreateView):
	form_class = UserCreationMultiForm
	template_name = "assimilate/register.html"
	success_url = reverse_lazy('registered')
	
	
	#def form_valid(self, form):
		# Save the user first, because the profile needs a user before it
		# can be saved.
	#	user = form['user'].save()
	#	profile = form['profile'].save(commit=False)
	#	profile.user = user
	#	profile.save()
		
		#return redirect(self.get_success_url())
	
	def reg(self, form):
		if self.request.method=="POST":
			#form=UserCreationMultiForm(request.POST)
			print("FORM ERRORS----",form.errors)
			if form.is_valid():
				new_user=form.save()
				print(self.request.user)
				
				#create a new session for new user
				#this is to pass the user info around across views (therefore, templates)
				self.request.session['form']=self.request.POST 
				
				#keep the user signed in after signing up
				new_user = authenticate(username=form.cleaned_data['user-username'],
		                            password=form.cleaned_data['user-password1'],
		                            )
				login(self.request, new_user)
				print(self.request.user)
				
				return redirect("registered")      
				
				
			else:
				messages.error(request, 'Oops. Something went wrong. Enter valid details!') 
				return redirect("register")
		else:
			form=UserCreationMultiForm(self.request.POST)	
			  
		return render(self.request, 'assimilate/register.html', {'form': form}) 
	
'''
	



'''
#NOPE 

#version 1
def register(request):
	if request.method=="POST":
		user_form=UserForm(request.POST)
		profile_form=ProfileForm(request.POST)
		#print(form.errors)
		if user_form.is_valid() and profile_form.is_valid():
			new_user=user_form.save()
			profile_form.save()
			print(request.user)
			request.session['form']=request.POST 
			
			#keep the user signed in after signing up
			new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
			login(request, new_user)
			print(request.user)
			
			return redirect("registered")      
			
			#form=User.objects.filter(user=request.user)
			#form=User.objects.get(pk=request.user.pk)
			#return redirect("registered",{'form':form})
			
		else:
			messages.error(request, 'Enter valid details!') 
			return redirect("register")
	else:
		user_form=UserForm(request.POST)
		profile_form=ProfileForm(request.POST)
		#return render(request,"assimilate/register.html",{"form":UserCreationForm()})  
	return render(request, 'assimilate/register.html', {'user_form': user_form, 'profile_form': profile_form}) 
'''

		
		
def registered(request):
	#print(request.user)
	#print(type(request.user))
	#print(request.user.username)
	
	
	#acquire the session info (created in register view)
	form = request.session.get('form') #to be able to say stakeholder/ domain expert based on what was entered while signing up
	print(form)
	
	
	
	#user = authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))   
	#request.user=form
	
	#request.user.username=form["username"]
	#request.user.password=form["password1"]
	#login(request, request.user)
	
	
	print(request.user)
	
	
	
	#del request.session['form']
	return render(request,"assimilate/registered.html",{'form':form})
	
	#return render(request,"assimilate/registered.html")#,{'form':form})	
	
	
	#return render(request,"assimilate/registered.html")	
	
	
		
class LoginView(View):
	def get(self,request):
		return render(request,"assimilate/login.html",{"form":AuthenticationForm()})
	def post(self,request):
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			print ("login logic")
			user = authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))  #if usn and pwd match with inst in db
			print(user)
			if user is None:
				messages.error(request, 'Enter valid username!')
				return redirect(request,"assimilate/login.html",{"form":form,"invalid_creds":True})
			login(request, user)
			return redirect(reverse('home_page'))
			#return redirect('post_list')
	
		else:
			messages.error(request, 'User not found! Invalid login!')
			print ("invalid login")
			return render(request,"assimilate/login.html",{"form":form,"invalid_creds":True})	
    
       
@login_required(login_url='login')     
def post_delete(request, pk):
    p = get_object_or_404(Post, pk=pk)
    p.delete()
    return redirect('post_list')
    
    
    
    
    
    
    
    
    
    
    
#*********************************************************************************************************

def first_page(request):
        return render(request,"assimilate/first_page.html")


#you need to be logged in to access this page
#if not logged in and you try to access this url, it'll redirect you to the login page
@login_required(login_url='login')
def home_page(request):
	print(request.user)
	return render(request, 'assimilate/home_page.html', {})

	
def browse(request):
	all_articles = Post.objects.filter(published_date__lte=timezone.now()).order_by('title')
	return render(request, 'assimilate/post_list.html', {'articles': all_articles})
	

@login_required(login_url='login')	
def edit_logs(request):
	edited_articles = EditLogs.objects.filter(user=request.user).order_by('-edited_date')
	return render(request, 'assimilate/edit_logs.html', {'edited_articles': edited_articles})
	
	

def search(request):

	query = request.GET['query']
	if len(query)>50:
		#allPosts = Post.objects.none()
		allPosts = ["too long"]
	else:
		allPostsTitle = Post.objects.filter(title__icontains=query)
		#print(allPostsTitle)
		allPostsContent = Post.objects.filter(content__icontains=query)
		#print(allPostsContent)
		allPostsDomain = Post.objects.filter(domain__iexact=query)
		#print(allPostsDomain)
		allPostsUser = Post.objects.filter(user__username__iexact=query)
		#print(allPostsUser)
		
		allPosts=[]
		if allPostsTitle:
			for post in allPostsTitle:
				allPosts.append(post)
		if allPostsContent:
			for post in allPostsContent:
				allPosts.append(post)
		if allPostsDomain:
			for post in allPostsDomain:
				allPosts.append(post)
		if allPostsUser:
			for post in allPostsUser:
				allPosts.append(post)
				
		#allPosts = allPostsTitle.union(allPostsContent)
		
		print("union list: ", allPosts)
		
		
		#remove duplicates
		allPosts=list(set(allPosts))
		print("duplicates removed: ", allPosts)
		
		'''
		for item in allPosts:
			print(item.published_date)'''
		
		#allPosts=allPosts.sort(key=date)
		
		#print(dict(allPosts))
		
		#allPosts=allPosts.sort(key=lambda post: post.published_date )
		
		allPosts=sorted(allPosts, key=lambda post: post.published_date )
		print("sorted list: ", allPosts)

	
	params = {'allPosts': allPosts, 'query':query}
	return render(request, 'assimilate/search_results.html', params)
	

def date(post):
	return post.published_date




