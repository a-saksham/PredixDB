from django.shortcuts import redirect, render
from .models import Movies, MyMovies, ContactUs
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random
from django.db.models import Count


def showIndexPage(request):
    mymovies = list(MyMovies.objects.all().values_list('mid', flat=True))
    latest = list(Movies.objects.order_by('-year').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    # hollywood = list(Movies.objects.filter(language__istartswith = 'english').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    # bollywood = list(Movies.objects.exclude(language__istartswith = 'english').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    mylist = list(MyMovies.objects.filter(uid__id__exact=request.user.id))
    movies = list(Movies.objects.all().filter(mid__isnull=False).filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    trending_m = set(MyMovies.objects.annotate(noccurence=Count('mid')).order_by('-noccurence').values_list('mid', flat='True'))
    if request.user.is_authenticated:
        trending = list(Movies.objects.filter(mid__in=trending_m).exclude(mymovies__uid=request.user))
    else:
        trending = list(Movies.objects.filter(mid__in=trending_m))
    random.shuffle(trending)
    random.shuffle(latest)
    # random.shuffle(hollywood)
    random.shuffle(movies)
    # random.shuffle(bollywood)
    return render(request, 'index.html', {'movies': movies, 'mylist': mylist, 'latest': latest, 'trending': trending})


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
            messages.success(request, "User Registered Successfully, please login to continue...")
            return redirect("/login/")
    return render(request, "signup.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def movieinfoPage(request):
    return render(request, 'movieinfo.html')


def aboutPage(request):
    return render(request, 'about.html')


def contactPage(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        if request.user.is_authenticated:
            uid = request.user.id
            user = User.objects.get(id=uid)
            query = ContactUs.objects.create(uid=user, name=name, email=email, subject=subject)
            query.save();
        else:
            query = ContactUs.objects.create(name=name, email=email, subject=subject)
            query.save();
        messages.success(request, "Request submitted successfully, we will reach you shortly if needed.")
    return render(request, 'contact.html')


def addMovie(request, mid):
    uid = request.user.id
    user_id = User.objects.get(id=uid)
    movie = Movies.objects.get(mid=mid)
    ob = MyMovies.objects.create(uid=user_id, mid=movie, watched=True)
    ob.save();
    return redirect('/')

def addMovieFromSearch(request, mid, query):
    uid = request.user.id
    user_id = User.objects.get(id=uid)
    movie = Movies.objects.get(mid=mid)
    ob = MyMovies.objects.create(uid=user_id, mid=movie, watched=True)
    ob.save();
    mymovies = list(MyMovies.objects.all().values_list('mid', flat=True))
    obj = Movies.objects.filter(title__icontains=query).filter(cover__isnull=False).exclude(mid__in=mymovies)
    other = list(Movies.objects.order_by('-rdate').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    return render(request, 'search.html', {'movies': obj, 'other': other, 'query': query})


def searchPage(request):
    srh = request.GET['query']
    mymovies = list(MyMovies.objects.all().values_list('mid', flat=True))
    obj = Movies.objects.filter(title__icontains=srh).filter(cover__isnull=False).exclude(mid__in=mymovies)
    other = list(Movies.objects.order_by('-rdate').filter(cover__isnull=False).exclude(mid__in=mymovies)[:50])
    return render(request, 'search.html', {'movies': obj, 'other': other, 'query': srh})