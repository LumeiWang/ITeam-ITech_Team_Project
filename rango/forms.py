from django import forms
from rango.models import News, Comment, Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
    help_text="Please enter the title of the page:")
    url = forms.URLField(max_length=200,
    help_text="Please enter the URL of the page:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Page
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class CommentForm(forms.ModelForm):
    content = forms.CharField( 
        help_text="Please enter the comment:",
        max_length=256,
    )
  
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Comment
        fields = ('content',)
        #exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
    help_text="Please enter the title of the news:")
    content = forms.CharField(max_length=512,
    help_text="Please enter the content of the news:")
    
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = News
        exclude = ('user','categoryID')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data