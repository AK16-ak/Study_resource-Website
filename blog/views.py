from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import  messages
from django.contrib.auth import  authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Home
def home(request):
    print('*********************----------- ',request.user)
    # print('*********************----------- ',Post.user)
    posts = Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# signup
def user_signup(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Signed up successfully!!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html',{'form':form})

# login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html',{'form':form})
    else:
       return HttpResponseRedirect('/dashboard/')


# Add New Post
def add_post(request):

    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                file_name=form.cleaned_data['file_name']
                my_file=form.cleaned_data['my_file']
                pst=Post(title=title,desc=desc,file_name=file_name,my_file=my_file)
                pst.save()
                print("Successfully posted--------------")
                form = PostForm()
            else:
                print("Failed posted--------Error------")

        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form=PostForm(instance=pi)
    
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# Search
def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allposts=Post.objects.none()
    else:

        titleposts= Post.objects.filter(title__icontains=query)
        contentposts= Post.objects.filter(desc__icontains=query)
        allposts= contentposts.union(titleposts)
    if allposts.count() == 0: 
        messages.warning(request,"Please enter valid serch text")
    params={'posts': allposts,'query': query}
    return render(request,'blog/search.html',params)