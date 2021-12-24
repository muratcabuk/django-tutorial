from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .forms import NewsForm
from .models import News, NewsCategory
from PIL import Image as Img
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    return render(request, "index.html")

def aboutus(request):
    return render(request, "about-us.html")

def contactus(request):
    return render(request, "contact-us.html")

def hotline(request):
    return render(request, "hotline.html")

def contexttest(request):
    # context key value şeklinde olmalı.
    # html tarafında her bir key tek başına çağrılarak kullanılır.
    # örnekler için context-test.html dosyasına bakınız
    context = {
        "yazar1":{"ad":"murat cabuk 1"},
        "yazar2": {"ad": "murat cabuk 2"},
        "yazar3": {"ad": "murat cabuk 3"},
        "yazar4": {"ad": "murat cabuk 4"},
        "yazar5": {"ad": "murat cabuk 5"},
        "listem":[1,2,3,4,5,6,[1,2,3,4]]

    }
    return render(request, "context-test.html", context=context)

def dynamicurltest(request,id):
    context = {"id":id}
    return render(request, "dynamic-url-test.html",context=context)
@login_required(login_url="/author/login")
def add(request):
    form = NewsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        news = form.save(commit=False)
        news.author = request.user
        news.save()
        messages.success(request,"makale başarıyla kaydedildi.")

        # farklı boyutlarda resim kaydetme başladı
        file_name = str(news.image_address.name).split("/")[1].split(".")[0]

        end = str(news.image_address.path).find(file_name)
        file_path = str(news.image_address.path)[0:end]

        image = Img.open(news.image_address.path)

        __resim_kaydet(image,file_path,file_name,200,200)
        __resim_kaydet(image,file_path,file_name,400,400)
        # farklı boyutlarda resim kaydetme başladı


        return redirect("author:author.profile")

    return render(request, "news/add.html",{"form" : form})

def __resim_kaydet(image, file_path, file_name, new_width, new_height):

    width, height = image.size  # Get dimensions

    left = round((width - new_width) / 2)
    top = round((height - new_height) / 2)
    x_right = round(width - new_width) - left
    x_bottom = round(height - new_height) - top
    right = width - x_right
    bottom = height - x_bottom

    # Crop the center of the image
    image = image.crop((left, top, right, bottom))

    image_size = "_" + str(new_width) + "x" + str(new_height) + ".jpg"
    image.save(file_path + file_name + image_size, format='JPEG', quality=75)

def list(request):
    news=News.objects.filter(author=request.user)
    context = {
        "news": news
    }
    return render(request, "news/list.html",context=context)

def edit(request, id):
    news = get_object_or_404(News, id=id)
    form = NewsForm(request.POST or None, instance=news)

    if form.is_valid():
        news = form.save(commit=False)
        news.author = request.user
        news.save()
        messages.success(request,"makale başarıyla değiştirildi.")
        return redirect("news:news.detail", str(id))

    return render(request,"news/edit.html", {"form":form})

def delete(request,id):
    news = get_object_or_404(News, id=id)
    news.delete()
    messages.success(request,"Haber başarıyla silindi")
    return redirect("news:news.list")

def detail(request,id):
    news = News.objects.filter(id=id).first() # get_object_or_404 fonksiyonu da kullanılabilirdi.
    context = {
        "news": news
    }
    return render(request, "news/detail.html", context=context)


def search(request):
    news_title = request.GET.get("q")
    news_category_id = request.GET.get("cid")
    page_number = request.GET.get('p')

    news = []
    query = Q(None) # Q objesi ile Or ve AND gibi birbirine bağlı sorgular yazabiliyoruz.
    if news_title or news_category_id:
        if news_title:
            text_list = str(news_title).split(" ")
            query = Q(title__contains=text_list[-1])
            for text in text_list[:-1]:
                query |= Q(title__contains=text)
        if news_category_id:
            news_category_id = int(request.GET.get("cid"))
            query |= Q(news_category_id=news_category_id)

        news = News.objects.filter(query).distinct()

        if page_number == None:
            page_number=1

        paginator = Paginator(news, 2)  # her sayfada 2 kayıt göterecek şekilde ayarlamış olduk
        news = paginator.get_page(page_number) # news objemiz artık haberler dışında sayfalam ile ilgili verileri de tutuyor

    categories = NewsCategory.objects.all()

    context = {
        "news":news,
        "categories":categories,
        "q":news_title, # arama kelimelerini ve haber kategori'id sini sayfalama linklerinde kullanabilmek için sayfaya geri gönderiyoruz.
        "cid":news_category_id

    }
    return render(request, "news/search.html",context=context)