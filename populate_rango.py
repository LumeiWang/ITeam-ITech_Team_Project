import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
import django
django.setup()
from rango.models import Category, Page

def populate():
    Athletics_pages = [
        {'title': 'Tokyo Olympics: Dina Asher-Smith says 100m came just a few weeks too early',
        'url':'https://www.bbc.co.uk/sport/olympics/58099137',
        'views': 132},
        {'title':'Poland’s David Tomala wins men’s 50km race walk',
        'url':'https://olympics.com/tokyo-2020/en/news/poland-david-tomala-wins-men-50km-race-walk',
        'views': 264},
        {'title':"Italian double delight as Antonella Palmisano wins gold in women's 20k walk",
        'url':'https://olympics.com/tokyo-2020/en/news/italian-double-delight-as-antonella-palmisano-wins-gold-in-women-s-20k-walk',
        'views': 376},
        {'title':'Canada’s Andre de Grasse gets hands on 200m gold medal adding to Rio 2016 silver',
        'url':'https://olympics.com/tokyo-2020/en/news/canada-s-andre-de-grasse-wins-200m-gold',
        'views': 370} ]
    
    Diving_pages = [
        {'title':'Tom Daley goes for gold in individual 10m platform',
        'url':'https://olympics.com/tokyo-2020/en/news/diving-tom-daley-goes-for-gold-in-10m-platform',
        'views': 199},
        {'title':"QUAN Hongchan, 14, scores perfect tens to win women's 10m platform diving gold",
        'url':'https://olympics.com/tokyo-2020/en/news/quan-hongchan-14-scores-three-tens-to-win-women-s-10m-platform-diving',
        'views': 402},
        {'title':"Tokyo Olympics: China's Quan Hongchan, 14, wins diving gold with three 10s",
        'url':'https://www.bbc.co.uk/sport/av/olympics/58098855',
        'views': 1165} ]
    
    Weightlifting_pages = [
        {'title':'Hidilyn Diaz: "This gold is for all Filipino people"',
        'url':'https://olympics.com/tokyo-2020/en/news/videos/hidilyn-diaz-this-gold-is-for-all-filipino-people',
        'views': 169},
        {'title':"Weightlifting - Women's +87kg Final",
        'url':'https://www.bbc.co.uk/programmes/p09py5fd',
        'views': 802},
        {'title':'Day 11: Red Button - Weightlifting',
        'url':'https://www.bbc.co.uk/programmes/m000ylyr',
        'views': 802} ]
    
    Tennis_pages = [
        {'title':'Stefanos Tsitsipas and his special Olympic memory',
        'url':'https://olympics.com/tokyo-2020/en/news/videos/stefanos-tsitsipas-and-his-special-olympic-memory',
        'views': 279},
        {'title':'Exclusive: With memories of Cathy Freeman’s golden moment, Ashleigh Barty eyes her own in Olympic debut',
        'url':'https://olympics.com/tokyo-2020/en/news/videos/exclusive-with-memories-of-cathy-freeman-s-golden-moment-ashleigh-barty-eyes-her',
        'views': 1002} ]

    Swimming_pages = [
        {'title':"Gold for USA's Murphy in Men's 100m Back",
        'url':'https://olympics.com/tokyo-2020/en/news/videos/gold-for-usa-s-murphy-in-men-s-100m-back',
        'views': 155},
        {'title':'Swimming - Medals Session',
        'url':'https://www.bbc.co.uk/programmes/p09pjzp5',
        'views': 643} ]
    
    cats = {'Athletics': {'pages': Athletics_pages, 'views': 128, 'likes': 64},
            'Diving': {'pages': Diving_pages, 'views': 64, 'likes': 32},
            'Weightlifting': {'pages': Weightlifting_pages, 'views': 32, 'likes': 16},
            'Tennis': {'pages': Tennis_pages, 'views': 64, 'likes': 32},
            'Swimming': {'pages': Swimming_pages, 'views': 64, 'likes': 32} }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()