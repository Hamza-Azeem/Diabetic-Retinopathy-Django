from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404
import random
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django. contrib import messages
from django.core.exceptions import PermissionDenied
# *************************** MODEL IMPORTS ***************************
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import warnings
warnings.filterwarnings("ignore")
from keras.models import load_model
# *************************** MODEL IMPORTS ***************************
WORKERS = 2
CHANNEL = 3
IMG_SIZE = 224
NUM_CLASSES = 5
SEED = 77
TRAIN_NUM = 1000 # use 1000 when you just want to explore new idea, use -1 for full train

def edit_profile_info(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        mobile_number = request.POST['mobile_number']
        user = request.user
        first_name = first_name.lower().title()
        last_name = last_name.lower().title()
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        account = Account.objects.get(user=user)
        account.mobile_number = mobile_number
        account.age = age
        account.save()
        return render(request, 'retinoscope/profile2.html', {'success': 'Information updated!'})
    else:
        return render(request, 'retinoscope/edit_profile.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect("index")

def activeEmail(request, user, to_email):
    mail_subject = "Activate your Retinascope account."
    message = render_to_string('retinoscope/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f' Dear {user}, A verification link has been sent to your email {to_email}. Please check your inbox and spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}. Check if you typed it correctly.')


def signup(request):
    if not(request.user.is_authenticated):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                try:
                    u = User.objects.get(username=username)
                    return render(request, 'retinoscope/signup.html', {'error_msg': 'Username already exists, Try Differnet one'})
                except:
                    try:
                        u = User.objects.get(email=email)
                        return render(request, 'retinoscope/signup.html', {'error_msg': 'Email already registerd with different account, Try Differnet one'})
                    except:
                        user = form.save(commit=False)
                        user.is_active = False
                        user.first_name = user.first_name.lower().title()
                        user.last_name = user.last_name.lower().title()
                        user.save()
                        account = Account(user=user, mobile_number=request.POST['mobile_number'], age=request.POST['age'])
                        account.save()
                        activeEmail(request, user, form.cleaned_data.get('email'))
                        return redirect('signup')
        else:
            form = UserRegisterForm()
    else:
        raise PermissionDenied()
    return render(request, 'retinoscope/signup.html', {'form': form})


# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         try:
#             u = User.objects.get(username=username)
#             return render(request, 'retinoscope/signup2.html', {'error_msg': 'Username already exists, Try Differnet one'})
#         except:
#             try:
#                 u = User.objects.get(email=email)
#                 return render(request, 'retinoscope/signup2.html', {'error_msg': 'Email already registerd with different account, Try Differnet one'})
#             except:
#                 password1 = request.POST['password1']
#                 password2 = request.POST['password2']
#                 if(password1 != password2):
#                     return render(request, 'retinoscope/signup2.html', {'error_msg': "Passwords don't match, Try again!"})
#                 else:
#                     age = request.POST['age']
#                     phonenumber = request.POST['phonenumber']
#                     user = User.objects.create_user(username=username, email=email, password=password1)
#                     user.save()
#                     account = Account(user=user, age=age, mobile_number=phonenumber)
#                     account.save()
#                     return render(request, 'retinoscope/home.html', {'msg': 'Account created successfully!'})
#     else:
#         return render(request, "retinoscope/signup2.html")




def index(request):
    return render(request, "retinoscope/home.html")

def logout(request):
    user_logout(request)
    return render(request, "retinoscope/home.html")

def profile(request, pk):
    if request.user.id  != pk:
        raise PermissionDenied
    else:
        u = get_object_or_404(User, pk=pk)
        account = get_object_or_404(Account, user_id=pk)
        return render(request, "retinoscope/profile2.html", {"user": u,
                                                        "account": account})


def change_password(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == "POST":
        old_password = request.POST['old_password']
        username = request.user.username
        user = authenticate(username=username, password=old_password)
        if user is not None:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if(password1 != password2):
                return render(request, 'retinoscope/change_password.html', {'error_msg': "Passwords don't match, Try again!"})
            else:
                user = User.objects.get(username=username)
                user.set_password(password1)
                user.save()
                user_login(request, user)
                return render(request, 'retinoscope/profile2.html', {'success': "Your password has been changed!"})
        else:
            return render(request, "retinoscope/change_password.html", {'error_msg':'Old password is incorrect'})

    else:
        return render(request, "retinoscope/change_password.html")

            

def get_history(request, pk):
    if pk != request.user.id:
        raise PermissionDenied
    else:
        account = get_object_or_404(Account, user_id=pk)
        history_list = account.history_set.all().order_by('-date')
        empty = len(history_list)
        return render(request, "retinoscope/history2.html", {"history_list": history_list,
                                                            "empty": empty,
                                                            'class0':0,
                                                            'class1':1,
                                                            'class2':2,
                                                            'class3':3,
                                                            'class4':4})
def somefunction():
    x = random.randint(0, 4)
    account = get_object_or_404(Account, user_id=79)
    account.history_set.create(date=timezone.now(), result=x)

def get_image(request, pk):
    if request.user.id  != pk:
        raise PermissionDenied
    result = -1
    if request.method == 'POST':
        u_image = request.FILES['image']
        result = classify(u_image)
        account = get_object_or_404(Account, user_id=pk)
        account.history_set.create(date=timezone.now(), result=result)
        return render(request, 'retinoscope/classify.html', {'result': result})
    else:
        return render(request, 'retinoscope/classify.html', {'result': result})

def load_ben_color(u_image, sigmaX=10):
    image_data = np.asarray(bytearray(u_image.read()), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = cv2.addWeighted(image, 4, cv2.GaussianBlur(image, (0, 0), sigmaX), -4, 128)
    return image

def classify(u_image):
    x = load_ben_color(u_image,sigmaX=50)
    image_array = image.img_to_array(x)
    image_arr_expanded = np.expand_dims(image_array, axis=0)
    processed_image = tf.keras.applications.mobilenet.preprocess_input(image_arr_expanded)
    model = load_model("D:\\Hamza\\College\\LAST_YEAR\\2nd_Semester\\project\\grad_site\\retinoscope\\mobilenett2.h5")
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions)
    return predicted_class



