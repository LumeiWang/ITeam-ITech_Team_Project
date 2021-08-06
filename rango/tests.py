import os
from django.test import TestCase
from django.urls import reverse
from populate_rango import populate
from django.contrib.auth.models import User
from django.forms import fields as django_fields

from rango import forms
from rango.models import Page, Category, Comment, News
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, CommentForm

# Create your tests here.

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class Test_Category(TestCase):
    """
    Check whether the category contains the expected elements. succussful
    """
    def test_category(self):
        """
        Check the likes and views are concluded.
        Check the page link is concluded.
        """
        populate()
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('rango:category'))

        content = response.content.decode()
        self.assertTrue('<a href' in content,
                        f"{FAILURE_HEADER}There is no hyperlinks to original page.{FAILURE_FOOTER}")
        self.assertTrue('<th>Views</th><th>Likes</th>' in content, 
                        f"{FAILURE_HEADER}There is views and likes shown in website.{FAILURE_FOOTER}")
       
class Test_News(TestCase):
    """
    Check whether the category contains the expected elements, failured by reverse.
    """
    def test_category(self):
        """
        Check the add-news' and add-page's functions are concluded.
        Check the page link is concluded.
        Check the comment function is concluded.
        """
        populate()
        user_object = create_user_object()
        c = self.client.login(username='testuser', password='testabc123')

        #response = self.client.get(reverse('rango:category',args=['diving']))
        response = self.client.get('category/<slug:category_name_slug>/')
        #response = self.client.get(reverse('rango:category', 
        #                           kwargs={'category_name_slug': 'diving'}))
        

        content = response.content.decode()
        print(content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="add_page"' in content,
                        f"{FAILURE_HEADER}There is no hyperlinks to original page.{FAILURE_FOOTER}")
        self.assertTrue('id="add_page"' in content, 
                        f"{FAILURE_HEADER}There is views and likes shown in website.{FAILURE_FOOTER}")
       
