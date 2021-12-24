from django.urls import path
from news import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "news"

urlpatterns = [
    path('index', views.index, name="news.index"), # ansayfa indexi ile news/index i
                                               # aynı sayfayı sogtereccek şekilde ayarlamış olduk.
                                               # buya ileride news/create, news/detail vb sayfalarda gelecek
    path('', views.index, name="news.empty"),
    path('dynamic-url-test/<int:id>', views.dynamicurltest, name="news.dynamicurltest"),
    path('add', views.add, name="news.add"),
    path('list', views.list, name="news.list"),
    path('edit/<int:id>', views.edit, name="news.edit"),
    path('delete/<int:id>', views.delete, name="news.delete"),
    path('detail/<int:id>', views.detail, name="news.detail"),
    path('search', views.search, name="news.search"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print(urlpatterns)