from django.contrib import admin

# Register your models here.

from .models import NewsCategory
from .models import News

# admin.site.register(NewsCategory)
# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "author", "created_date"]
    search_fields = ["title"]
    list_filter = ["created_date",  "news_category_id"]

    class Meta:
        model = News



@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "author", "created_date"]
    search_fields = ["title"]
    list_filter = ["created_date"]

    class Meta:
        model = NewsCategory










