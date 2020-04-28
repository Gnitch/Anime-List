from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Post, Links, AnimeInfo
from .forms import PostForm, UserSignUpForm, UserAuthenticationForm
from .Scrap import Scrap

def userLogout(request):
    logout(request)
    return redirect('/blogApp/')

def userLogin(request):
    if request.method == 'POST' :
        form =  UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None :
                print("User Authenticated")
                login(request, user)
                user_id = user.id
                blogs_list = Post.objects.filter(author_id=user_id)
                # context={'user': user}
                context = {'blogs_list':blogs_list}
                return render(request,'blog/home.html',context)
            else :
                form =  UserAuthenticationForm()
                message = ''
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'blog/login.html',context)    

        else :
            form =  UserAuthenticationForm()
            message = 'Invalid Username or Password'
            type_form = 'login'
            context = {'form':form,'message':message,'type_form':type_form}
            return render(request,'blog/login.html',context)   

    else :
        form =  UserAuthenticationForm()
        message = ''
        type_form = 'login'
        context = {'form':form,'message':message,'type_form':type_form}
        return render(request,'blog/login.html',context)  


def userSignUp(request):
    if request.method == 'POST' :
        form =  UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')

            if(password1 == password2):
                if User.objects.filter(username=username).exists():
                    form =  UserSignUpForm(request.GET)                
                    message = 'Username already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'blog/login.html',context)
        
                elif User.objects.filter(email=email).exists():
                    form =  UserSignUpForm(request.GET)
                    message = 'Email already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'blog/login.html',context)

                else :
                    user = User.objects.create_user(username=username,password=password1,email=email)
                    user.save()
                    user = authenticate(request, username=username, password=password1)
                    if user is not None :
                        print("User registered and authenticated")
                        login(request, user)
                        user_id = user.id
                        # print(user_id)
                        blogs_list = Post.objects.filter(author_id=user_id)
                        context={'blogs_list': blogs_list}
                        return render(request,'blog/home.html',context)
                    else :
                        form =  UserAuthenticationForm()
                        message = 'User authentcation failed'
                        type_form = 'login'
                        context = {'form':form,'message':message,'type_form':type_form}
                        return render(request,'blog/login.html',context)

            else :
                    form =  UserSignUpForm(request.GET)
                    # form =  UserCreationForm(request.POST)
                    message = 'Passwords do not match'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'blog/login.html',context)

        else :
                form =  UserSignUpForm(request.GET)
                # form =  UserCreationForm(request.POST)
                message = 'Passwords do not match'
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'blog/login.html',context)

    else :
        form = UserSignUpForm(request.GET)
        message=''
        type_form='signup'
        context = {'form':form,'message':message,'type_form':type_form}
        return render(request,'blog/login.html',context)

@login_required
def home_page(request, user_id):
    blogs_list = Post.objects.filter(author_id=user_id)
    context={'blogs_list': blogs_list}
    return render(request,'blog/home.html',context)

@login_required
def aboutPage(request):
    return render(request,'blog/About.html')

@login_required
def searchResults(request, user_id):
    if request.method == 'GET' :
        query = str(request.GET.get('q'))
        blogs_list = Post.objects.filter(author_id=user_id).filter(title__icontains=query)
    link = 'search'
    context={'blogs_list': blogs_list,'link':link}
    return render(request,'blog/home.html',context)

@login_required
def watching(request, user_id):
    blogs_list= list(Post.objects.filter(author_id=user_id).filter(status='watching'))
    link = "'watching'"
    context={'blogs_list': blogs_list,'link':link}
    return render(request,'blog/home.html',context)

@login_required
def watched(request, user_id):
    blogs_list= list(Post.objects.filter(author_id=user_id).filter(status='watched'))
    link = "'watched'"
    context={'blogs_list': blogs_list,'link':link}
    return render(request,'blog/home.html',context)

@login_required
def notWatched(request, user_id):
    blogs_list= list(Post.objects.filter(author_id=user_id).filter(status='not watched'))
    link =  "'not watched'"
    context={'blogs_list': blogs_list,'link':link}
    return render(request,'blog/home.html',context)

@login_required
def blog_post(request,blog_post_id,user_id):
    linksObj = Links.objects.get(postId_id=blog_post_id)
    print(blog_post_id)
    AnimeInfoObj = AnimeInfo.objects.get(postId_id=blog_post_id)
    blog_object = get_object_or_404(Post, pk=blog_post_id)
    context={'blog_object': blog_object,'linksObj':linksObj,'AnimeInfoObj':AnimeInfoObj}
    return render(request,'blog/post.html',context)

@login_required
def completed(request, blog_post_id,user_id):
    linksObj = Links.objects.get(postId_id=blog_post_id)
    blog_object = get_object_or_404(Post, pk=blog_post_id)
    blog_object.status = 'watched'
    blog_object.save()
    context={'blog_object': blog_object,'linksObj':linksObj,}
    return render(request,'blog/post.html',context)

@login_required
def watching_btn(request, blog_post_id,user_id):
    linksObj = Links.objects.get(postId_id=blog_post_id)
    blog_object = get_object_or_404(Post, pk=blog_post_id)
    blog_object.status = 'watching'
    blog_object.save()
    context={'blog_object': blog_object,'linksObj':linksObj}
    return render(request,'blog/post.html',context)

@login_required
def createNewPost(request, user_id):
    if request.method == 'POST' :
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                scrapObj = Scrap(title)
                desc, genre_anime, episode_list, op_list, ed_list =  scrapObj.scrap()
                instance = form.save(commit=False)
                instance.author_id=user_id
                instance.body = desc
                instance.genre = genre_anime
                instance.save()
                print("valid")
                saveLinks(str(title))
                saveAnimeInfo(str(title),episode_list,str(op_list),str(ed_list))

    form = PostForm()
    return render(request,'blog/NewPost.html',{'form':form})

@login_required
def header(request):
    return render(request,'blog/header.html')


@login_required
def profile(request, user_id):
    user = User.objects.get(pk = user_id)
    print(user.email)
    context = {'user':user}
    return render(request, 'blog/profile.html',context)


def saveLinks(title):
    
    newS = ''
    for each in title :
        if(each != ' '):
            newS = newS + each      
        else :
            newS = newS + str('+')

    postObj = Post.objects.get(title=title)
    kaizoku_url = 'https://animekaizoku.com//?s='+str(newS)
    anidl_url = 'https://anidl.org//?s='+str(newS)
    linksObj = Links.objects.create(
        animeKaizoku = kaizoku_url,
        anidl = anidl_url,
        postId_id = postObj.id
    )
    linksObj.save()

def saveAnimeInfo(title, episodes, oP_list, eD_list) :
    postObj = Post.objects.get(title=title)
    AnimeInfoObj = AnimeInfo.objects.create(
        episode_list=episodes,
        op_list=oP_list,
        ed_list = eD_list,
        postId_id = postObj.id
    )    
    AnimeInfoObj.save()


