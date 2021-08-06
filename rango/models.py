from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def pic_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return '/media/default_user.jpg'

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #page = models.ForeignKey(Page, on_delete=models.CASCADE)
    page = models.CharField(max_length=256)
    news = models.CharField(max_length=256)
    content = models.CharField(max_length=256)

    def __str__(self):
        return self.user.username

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=512)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=512)

    def __str__(self):
        return self.title

class Likepage(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    likepageid = models.IntegerField(null=True)


    def __str__(self): 
        return self.page.title + "(liked by " + self.user.username + ")" 