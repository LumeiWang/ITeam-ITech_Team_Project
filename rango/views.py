from django.db.models.fields import NullBooleanField
from django.db.models.fields.related_descriptors import create_reverse_many_to_one_manager
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.models import Comment
from rango.forms import CommentForm
from rango.models import News
from rango.forms import NewsForm
from rango.models import UserProfile, Likepage


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['ct1'] = category_list[0]
    context_dict['ct2'] = category_list[1]
    context_dict['ct3'] = category_list[2]

    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Cheng Ye'}
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)

def category(request):
    context_dict = {}
    category_list_like = Category.objects.order_by('-likes')
    category_list_views = Category.objects.order_by('-views')
    page_list = Page.objects.order_by('-views')

    context_dict['category_all_views'] = category_list_views
    context_dict['pages'] = page_list

    return render(request, 'rango/all_category.html', context=context_dict)
    
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        news = News.objects.filter(category=category.name)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['news'] = news
    
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['news'] = None
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                         kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def allpages(request):
    context_dict = {}
    page_list = Page.objects.order_by('-views')
    likepage_list = Likepage.objects.order_by('id')

    context_dict['pages'] = page_list
    context_dict['likepages'] = likepage_list
    context_dict['user'] = request.user


    return render(request, 'rango/all_pages.html', context=context_dict)


def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html', context = {'user_form': user_form,
                  'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

@login_required
def add_news(request, category_name_slug):
    if request.user.has_perm('rango.add_news')==False:
        return redirect('/rango/')
    try:
        category = Category.objects.get(name=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/rango/')
    form = NewsForm()

    if request.method == 'POST':
        form = NewsForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category.name
                page.user = request.user
                page.save()
                return redirect(reverse('rango:show_category',
                                         kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_news.html', context=context_dict)

def show_comment(request, category_name_slug, title):
    context_dict = {}
    try:
        category = Category.objects.get(name=category_name_slug)
        page = Page.objects.get(title=title)    
        comments = Comment.objects.filter(pageID=page.id)
        context_dict['page'] = page
        context_dict['comments'] = comments
        context_dict['category'] = category
    
    except Page.DoesNotExist:
        page = News.objects.get(title=title)
        comments = Comment.objects.filter(newsID=page.id)
        context_dict['page'] = page
        context_dict['comments'] = comments
        context_dict['category'] = category
        
    return render(request, 'rango/comment.html', context=context_dict)

@login_required
def add_comment(request, category_name_slug, title):
    try:
        category = Category.objects.get(name=category_name_slug)
        page = Page.objects.get(title=title)
        count = 0
            
    except Page.DoesNotExist:
        page = News.objects.get(title=title)
        count = 1
    
    if page is None:
        return redirect('/rango/')

    form = CommentForm()    
    if request.method == 'POST':
        form = CommentForm(request.POST)      
        if form.is_valid():
            if page:
                comment = form.save(commit=False)
                if count == 0:
                    comment.pageID = page.id
                else :
                    comment.newsID = page.id
                comment.user = request.user
                comment.save()
                return redirect(reverse('rango:show_comment',
                                         kwargs={'category_name_slug':category_name_slug, 'title': title}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category, 'page':page}
    return render(request, 'rango/add_comment.html', context=context_dict)

def show_news(request, category_name_slug, title):
    context_dict = {}
    try:
        category = Category.objects.get(name=category_name_slug)
        news = News.objects.get(title=title)
        context_dict['news'] = news
        context_dict['category'] = category
    
    except Category.DoesNotExist:
        context_dict['news'] = None
        context_dict['category'] = None
    return render(request, 'rango/news.html', context=context_dict)


def user_info(request):
    context_dict = {}
    user = request.user
    news = News.objects.filter(user = user)
    comments = Comment.objects.filter(user = user)
    context_dict['user'] = user
    context_dict['news'] = news
    context_dict['comments'] = comments
    return render(request, 'rango/user.html', context=context_dict)

def delete(request, data):
    try:
        news = News.objects.get(id=data)
        News.objects.filter(id=data).delete()  
        return redirect('/rango/user/')

    except News.DoesNotExist:
        comment = Comment.objects.get(id=data)
        Comment.objects.filter(id=data).delete() 
        return redirect('/rango/user/')


def register_official(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            vi = Permission.objects.filter(codename='add_news')[0]
            user.user_permissions.add(vi)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,'rango/register_official.html', context = {'user_form': user_form,
                  'profile_form': profile_form, 'registered': registered})

def myaccount(request):
    user = request.user
    context_dict = {}
    if UserProfile.objects.filter(user=user):
        user_prof = UserProfile.objects.get(user=user)
        context_dict['user_url'] = user_prof.pic_url()
    else:
        context_dict['user_url'] = '/media/default_user.jpg'

    context_dict['user_base'] = user
    return render(request, 'rango/myaccount.html', context=context_dict)

#search all view
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    
    if not q:
        error_msg = 'please enter keywords'
        return render(request, 'rango/results.html', {'error_msg': error_msg})\

    context_dict = {}

    post_list = Page.objects.filter(title__icontains=q)
    categorypost_list = Category.objects.filter(name__icontains=q)
    newspost_list = News.objects.filter(title__icontains=q)
    context_dict['error_msg'] = error_msg
    context_dict['pages'] = post_list
    context_dict['cates'] = categorypost_list
    context_dict['news'] = newspost_list
    context_dict['searchword'] = q


    return render(request,'rango/results.html', context=context_dict)



#search category
def searchcategory(request):
    c = request.GET.get('c')
    error_msg = ''

    if not c:
        error_msg = 'please enter keywords'
        return render(request, 'rango/results.html', {'error_msg': error_msg})

    categorypost_list = Category.objects.filter(name__icontains=c)
    return render(request,'rango/results.html',{'error_msg':error_msg, 'categorypost_list':categorypost_list})


#search news
def searchnews(request):
    n = request.GET.get('n')
    error_msg = ''

    if not n:
        error_msg = 'please enter keywords'
        return render(request, 'rango/results.html', {'error_msg': error_msg})

    newspost_list = News.objects.filter(title__icontains=n)
    return render(request,'rango/results.html',{'error_msg':error_msg, 'newspost_list':newspost_list})

@login_required
def like_page(request, title): 
    context_dict = {} 
    current_user = request.user 
    page = Page.objects.get(title=title)    

    try: 
        #if like already exists,cancel this like 
        like = Likepage.objects.get(page = page,user = current_user) 
        like.delete() 
        page.likes -=1 
        page.save(update_fields=['likes']) 
        context_dict['like'] = None 
    except Likepage.DoesNotExist: 
        #if like didn't exists, add this like 
        page.likes+=1 
        page.save(update_fields=['likes']) 
        like = Likepage.objects.get_or_create(page = page,user = current_user) 
        context_dict['like'] = like 
    return redirect(reverse('rango:allpages')) 
