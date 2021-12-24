from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, RegexValidator

from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage

from ckeditor.fields import RichTextField

import uuid

# Create your models here.

# https://docs.djangoproject.com/en/4.0/topics/db/models/

class NewsCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar")
    title = models.CharField(max_length=255,  verbose_name="Başlık")
    desc = models.TextField( verbose_name="Açıklama")
    created_date=models.DateTimeField(auto_now_add=True,  verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Haber Kategori"
        verbose_name_plural = "Haber Kategorileri"


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    news_category_id = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name="Haber Kategorisi")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,  verbose_name="Yazar")
    title = models.CharField(max_length=255,  verbose_name="Başlık")
    # detail = models.TextField( verbose_name="Haber Detayı")
    detail = RichTextField()

    created_date=models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi",
                                      validators=[FileExtensionValidator(["jpg","jpeg","png"])])

    # files klasöründe  images klasörü altında
    image_address = models.FileField(upload_to='images',blank=True, null=True, verbose_name="Haber Resmi", help_text="Maksimum 5MB resim seçiniz")

    def save(self, *args, **kwargs):
        if self.image_address:
            image = Img.open(self.image_address)

            ###################################################### Thumbnail oluşturmak
            #image.thumbnail((200, 200), Img.LANCZOS) # LANCZOS resim küçültülürken kullanılacak algoritma,
                                                      # resmi 200x200 e sığdır
            #box = (0, 0, 200, 200) # x=0 y=0 dan x=200 y=200 e resimden bir kare al
            #image = image.crop(box)

            ###################################################### resmin tam ortasından resim oluşturmak
            # width, height = image.size  # Get dimensions
            # new_width = 200
            # new_height = 200
            #
            # left = round((width - new_width) / 2)
            # top = round((height - new_height) / 2)
            # x_right = round(width - new_width) - left
            # x_bottom = round(height - new_height) - top
            # right = width - x_right
            # bottom = height - x_bottom
            #
            # # Crop the center of the image
            # image = image.crop((left, top, right, bottom))


            output = BytesIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)

            image_name = str(uuid.uuid4().hex)
            self.image_address = InMemoryUploadedFile(output, 'ImageField', image_name+".jpg", 'image/jpeg',
                                              len(output.read()), None)



        super(News, self).save(*args, **kwargs)

    def delete (self, *args, **kwargs):
        try:
            image_address=self.image_address.path

            end = str(image_address).split("/")[-1].find(".jpg")
            file_name = str(image_address).split("/")[-1][0:end]

            end = str(image_address).find(file_name)
            file_path = str(image_address)[0:end]

            default_storage.delete(image_address)
            default_storage.delete(file_path + file_name + "_200x200.jpg")
            default_storage.delete(file_path + file_name +"_400x400.jpg")
        except:
            pass
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"

