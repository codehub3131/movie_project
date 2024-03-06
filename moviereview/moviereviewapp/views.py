from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

from moviereviewapp.forms import MovieForm, ReviewForm, UserForm
from moviereviewapp.models import Movies, Category, Review


# Create your views here.
def index(request):
    category_id = request.GET.get('category')
    if category_id:
        movies = Movies.objects.filter(categories__id=category_id)
    else:
        movies = Movies.objects.all()

    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories, 'page_obj': page_obj})

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return  redirect('login')
    return render(request,"login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                user.save()
                messages.success(request, f"Welcome, {user.username}! Your account has been created. Please log in.")
                return redirect('/')

        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')

    return render(request, "register.html")

def detail(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews})

def add_movie(request):
    if request.method == "POST":
        title = request.POST.get('title',)
        poster = request.FILES['poster']
        desc = request.POST.get('desc', )
        release = request.POST.get('release', )
        actors = request.POST.get('actors', )
        actress = request.POST.get('actress', )
        categories = request.POST.getlist('categories')
        trailer_link = request.POST.get('trailer_link', )
        movie = Movies(title=title, desc=desc, poster=poster, release=release, actors=actors, actress=actress, trailer_link=trailer_link)
        movie.user = request.user
        movie.save()
        return redirect('/')

    categories = Category.objects.all()
    return render(request, 'add.html', {'categories': categories})


def update(request, id):
    movie = Movies.objects.get(id=id)
    form = MovieForm(request.POST or None, request.FILES, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'form': form, 'movie': movie})

def delete(request,id):
    if request.method=="POST":
        movie=Movies.objects.get(id=id)
        movie.delete()
        return  redirect('/')
    return render(request,'delete.html')

def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movies.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("moviereviewapp:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'details.html', {"form": form})
    else:
        return redirect("login/")

@login_required
def view_profile(request):
    return render(request, 'view_profile.html')

@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('view_profile')

    return render(request, 'edit_profile.html', {'user_form': user_form})



def SearchResult(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    movies = Movies.objects.all()

    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(desc__icontains=query))

    if category_id:
        movies = movies.filter(categories__id=category_id)

    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'query': query, 'category_id': category_id, 'page_obj': page_obj})

