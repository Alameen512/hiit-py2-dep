from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from projectapp.models import Post
from projectapp.forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# Create your views here.

def home(request):
    # return HttpResponse("Welcome to my home page")
    return render(request, "index.html")

def about(request):
    about_message = """
    This is a message for the about page from the backend. 
    """
    best_players = [ "Neymar", "Mbappe", "Messi", "Dembele"]
    GOAT = "Ronaldo"
    context = {"dml": about_message, "prog_name": "DmlStack", "age": 43, "best_players": best_players, "GOAT": GOAT,}
    return render(request, "about.html", context)

def profile(request):
    me = {
        "name": "Favour",
        "class": "Python",
        "age": 54
    }
    return JsonResponse(me)

def posts(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts.html", context)

def post(request, pk):
    # the_post = Post.objects.get(pk = pk)
    the_post = get_object_or_404(Post, pk = pk)
    context = {"post": the_post}
    return render(request, "post.html", context)

def display_form(request):
    return render(request, "user_form.html")

def submit_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        dept = request.POST.get("department")

        values = {"name": name, "department": dept}
        return JsonResponse(values)
    return redirect("user_form")

def add_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:

        form = PostForm()

    context = {"post_form": form}
    return render(request, "post_form.html", context)


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid:
            form.save()
            return redirect("posts")
    else:
    
        form = PostForm(instance=post)

    context = {"post_form": form}
    return render(request, "post_form.html", context)


def create_user(request):

    
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            
            form.save()
            messages.success(request, "User Added Successfully")
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "create_user.html", context)

def custom_create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        #1- check that they're no empty inputs
        if not(username and email and password and confirm_password):
            messages.error(request, "All fields are required")
            return redirect("custom_create_user")

        is_valid = True
        #2- check if username exists
        if User.objects.filter(username__iexact = username).exists():
            messages.error(request, "Username taken")
            is_valid = False
        if User.objects.filter(email__iexact = email).exists():
            messages.error(request, "Email already taken")
            is_valid = False
        if password != confirm_password:
            messages.error(request, "Two passwords don't match")
            is_valid = False

        if is_valid ==False:
            return redirect("custom_create_user") 

        created_user = User.objects.create_user(username = username, email=email, password = confirm_password) 
        messages.success(request, f"Hi! {created_user.username}! Your account has been created!") 
        return redirect("login")
    return render (request, "custom_create_user.html")



def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {
        "students": students
    })


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(request, "students/student_form.html", {
        "form": form
    })

@login_required(login_url="login")
def student_update(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_form.html", {
        "form": form
    })


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(request, "students/student_confirm_delete.html", {
        "student": student
    })

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('home')  # redirect to your home page
#     else:
#         form = AuthenticationForm()
#     return render(request, 'auth/login.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid login credentials")
            return redirect ("login")

        auth.login(request,user)
        return redirect("home")
    return render(request, "auth/login.html")

def logout (request):
    auth.logout(request)
    return redirect("login")