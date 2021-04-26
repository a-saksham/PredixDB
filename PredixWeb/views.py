from django.shortcuts import redirect, render
from .models import Movies, MyMovies
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random

def showIndexPage(request):
    mymovies = list(MyMovies.objects.all().values_list('mid', flat=True))
    latest = list(Movies.objects.order_by('-rdate').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    hollywood = list(Movies.objects.filter(language__istartswith = 'english').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    bollywood = list(Movies.objects.exclude(language__istartswith = 'english').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    mylist = list(MyMovies.objects.filter(uid__id__exact=request.user.id))
    movies = list(Movies.objects.all().filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    
    random.shuffle(latest)
    random.shuffle(hollywood)
    random.shuffle(movies)
    random.shuffle(bollywood)
    
    return render(request, 'index.html', {'movies': movies, 'mylist': mylist, 'latest': latest, 'hollywood': hollywood, 'bollywood': bollywood})

def loginPage(request):
    if request.method=='POST':
        uname = request.POST['uname']
        password = request.POST['password']
        user = auth.authenticate(username=uname, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'invalid credentials or user not registered...')
            
    return render(request, 'login.html')

def signupPage(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        uname = request.POST['uname']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username taken, please use different username...")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email ID already registered, please try to login...")
        else:
            user = User.objects.create_user(username=uname, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save();
            print('user created')
            messages.success(request, "User Registered Successfully, please login to continue...")
            return render(request, "login.html")
    return render(request, "signup.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def movieinfoPage(request):
    return render(request, 'movieinfo.html')

def aboutPage(request):
    return render(request, 'about.html')

def contactPage(request):
    return render(request, 'contact.html')

def addMovie(request, mid):
    uid = request.user.id
    user_id = User.objects.get(id=uid)
    movie = Movies.objects.get(mid=mid)
    ob = MyMovies.objects.create(uid=user_id, mid=movie, watched=True)
    ob.save();
    return redirect('/')

def searchPage(request):
    srh = request.GET['query']
    obj = Movies.objects.filter(title__icontains=srh).filter(cover__isnull=False)


    mymovies = list(MyMovies.objects.all().values_list('mid', flat=True))
    other = list(Movies.objects.order_by('-rdate').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    return render(request, 'search.html', {'movies': obj, 'other': other})