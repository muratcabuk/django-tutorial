from django.forms import ModelForm,TextInput, Select, Textarea
from .models import News

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['news_category_id', 'title', 'detail',"image_address" ]
        widgets = {
            'news_category_id': Select(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': "form-control"}),
            'detail': Textarea(attrs={'class': 'form-control'}),
            #'image_address': Textarea(attrs={'class': 'form-control form-control-sm'}),
            }