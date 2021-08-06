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
        
        class CommentFunction(TestCase):
    """
    Tests that the comment-related functions are working correctly
    """

    def test_comments(self):
        """
        Check that the added comment entries are displayed correctly
        """
        populate()
        test_user = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        test_page = Page.objects.get(url='https://olympics.com/tokyo-2020/en/news/videos/gold-for-usa-s-murphy-in-men-s-100m-back')

        test_data = {'content': 'All the athletes have worked hard'}
        test_comment_form = CommentForm(data=test_data)

        self.assertTrue(test_comment_form.is_valid(),
                        f"{FAILURE_HEADER}The CommentForm was not valid after entering the required data.{FAILURE_FOOTER}")

        test_comment = test_comment_form.save(commit=False)
        test_comment.page = test_page
        test_comment.user = test_user
        test_comment.save()

        response = self.client.get(reverse('rango:comment', kwargs={'category_name_slug': 'Swimming',
                                                                      'page_title_slug': "Gold for USA's Murphy in Men's 100m Back"}))
        content = response.content.decode()
        self.assertTrue('testuser' in content,
                        f"{FAILURE_HEADER}The comment do not successfully display.{FAILURE_FOOTER}")
        self.assertTrue('All the athletes have worked hard' in content,
                        f"{FAILURE_HEADER}The comment do not successfully display.{FAILURE_FOOTER}")

    def test_comment_form(self):
        """
        Tests whether CommentForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('CommentForm' in dir(forms),
                        f"{FAILURE_HEADER}We couldn't find the CommentForm class in Rango's forms.py module.{FAILURE_FOOTER}")

        comment_form = forms.CommentForm()
        self.assertEqual(type(comment_form.__dict__['instance']), 
                         f"{FAILURE_HEADER}Your CommentForm does not match up to the Comment model. {FAILURE_FOOTER}")

        fields = comment_form.fields

        expected_fields = {
            'content': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(),
                            f"{FAILURE_HEADER}The field {expected_field_name} was not found in the CommentForm form.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]),
                             f"{FAILURE_HEADER}The field {expected_field_name} in CommentForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

       
