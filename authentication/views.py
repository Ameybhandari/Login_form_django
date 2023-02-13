from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Login_form import settings
from django.core.mail import send_mail


# Create your views here.

def home(request):
    return render(request, "authentication/home.html")

def signout(request):
    logout(request)
    return redirect(home)

def signup(request):

    if request.method == "POST":
        username = request.POST['Username']
        f_name = request.POST['F_Name']
        l_name = request.POST['L_Name']
        email = request.POST['Email_Id']
        pass1 = request.POST['Password']
        pass2 = request.POST['C_Password']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists')
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request, 'Email already exists')
            return redirect('home')

        if len(username)>10:
            messages.error(request, "Username must be under 10 charectors")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('home')

        

        # Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = f_name
        myuser.last_name = l_name
        # Keeping the user account deactivated for now
        myuser.is_active = False

        # Save User
        myuser.save()

        # Succcess message
        messages.success(request, "Your account has been created successfully")

        # Welcome email 

        subject = "Welcome to the django Login!"
        message = "Hello " + myuser.first_name + " !! \n"+ "Welcome to django project!! \n" + "Thank you for visiting our website \n"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently= True)


       
        return redirect('home')
        
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username= username, password= password)
        # Not none is returned if the authentication is successful
        if user is not None: 
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/home.html",{'fname':fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")



