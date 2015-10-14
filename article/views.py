from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed #RSS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加包-分页

# Create your views here.
##def home(request):
##    return HttpResponse("Hello World, My First Django")

def home(request):
    post_list = Article.objects.all()  #获取全部的Article对象
    return render(request, 'home.html', {'post_list' : post_list})

def detail_test(request, my_args):
    return HttpResponse("You're looking at my_args~~~~~ %s." % my_args)

##def detail(request, my_args):
##    #如何读取入数字，http://127.0.0.1:8000/1/
##    post = Article.objects.all()[int(my_args)]
##
##    #读取出的数据库内容显示格式设置
##    str = ("title = %s, category = %s, date_time = %s, content = %s" 
##        % (post.title, post.category, post.date_time, post.content))
##    return HttpResponse(str)

#活动页显示每一篇文章
def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post})

def test(request) :
    return render(request, 'test.html', {'current_time': datetime.now()})

#归档：列出当前博客中所有的文章, 并且能够显示时间
def archives(request) :
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'archives.html', {'post_list' : post_list, 'error' : False})

#About Me
def about_me(request) :
    return render(request, 'aboutme.html')

#标签分类
def search_tag(request, tag) :
    try:
        post_list = Article.objects.filter(category__iexact = tag) #contains
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

#查询
def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'home.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0 :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : True})
            else :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : False})
    return redirect('/')

#RSS
class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

#分页
def home(request):
    posts = Article.objects.all()  #获取全部的Article对象
    paginator = Paginator(posts, 3) #每页显示两个
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list' : post_list})
