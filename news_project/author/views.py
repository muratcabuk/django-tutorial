from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login as log_in, authenticate, logout as log_out
from django.contrib import messages

# Create your views here.
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password) # kullanıcının veritabanında olup olmadığını
                                                                  # kendimiz kontrol ediyoruz
        if user is None:
            messages.error(request=request, message = "Kullanıcıadı veya şifre bulunamadı!")
            context = {"form": form}
            return render(request, "author/login.html", context=context)

        messages.success(request, 'Başarıyla giriş yaptınız')
        log_in(request, user)
        return redirect("author:author.profile")

    context = {"form": form}
    return render(request, "author/login.html", context=context)

def logout(request):
    log_out(request)
    messages.success(request,"başarıyla çıkış yaptınız!")
    return render(request, "author/logout.html")

def register(request):

    #####################################33 üçüncü son versiyon - en kısa yazım
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username") # burada get içindeki key ler forms.py
                                                     # doyasında return ettiğimiz key lerle aynı olmalı
        password = form.cleaned_data.get("password")
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        log_in(request, new_user) # register olan kullanıcıyı sisteme aynı zamanda login yaptık
                             # https://docs.djangoproject.com/en/4.0/topics/auth/default/
        messages.success(request, 'Başarıyla giriş yaptınız')

        return redirect("author:author.profile") # buradaki index urls.py dosyasında veridiğimiz name
        # scrf e takılmamak için register.html deki form tag'inin içine {% csrf_token %} ekledik
    context = {"form": form}
    return render(request, "author/register.html", context=context)



    ###################################### ikinci versiyon hem get hem de poat metodları chek edildi
    # if request.method == "POST":
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username") # burada get içindeki key ler forms.py
    #                                                      # doyasında return ettiğimiz key lerle aynı olmalı
    #         password = form.cleaned_data.get("password")
    #         new_user = User(username=username)
    #         new_user.set_password(password)
    #         new_user.save()
    #         log_in(request, new_user) # register olan kullanıcıyı sisteme aynı zamanda login yaptık
    #                              # https://docs.djangoproject.com/en/4.0/topics/auth/default/
    #
    #         return redirect("author:author.profile") # buradaki index urls.py dosyasında veridiğimiz name
    #         # scrf e takılmamak için register.html deki form tag'inin içine {% csrf_token %} ekledik
    #
    #     context = {"form": form}
    #     return render(request, "author/register.html", context=context)
    #
    # else:
    #     form = RegisterForm()
    #     context = {"form" : form}
    #     return render(request, "author/register.html", context=context)

    ###################################### ilk versiyonda post get ayrımı yoktu sade get vardı
    # form = RegisterForm()
    # context = {
    #     "form" : form
    # }
    # return render(request, "author/register.html", context=context)

def profile(request):
        return render(request, "author/profile.html")

