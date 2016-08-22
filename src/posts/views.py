try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext

import re
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post

def about(request):
    return render(request,'about.html')

def category(request):
    return render(request,'Home.html')

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request,slug,year,month):
    instance = get_object_or_404(Post,publish__year=int(year), publish__month=int(month),slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type= content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
            )
        subject = ' Comment recieved - " '+instance.title[0:50] +'.. ."'
        message = ' Post Title : '+instance.title +'. \n Comment : '+str(content_data)+'. \n User : '+str(request.user)
        sender = ''
        recipients = ['mail2raajj@gmail.com']
        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    posts,pagedata = init()
    queryset_list = Post.objects.active() #.order_by("-timestamp")

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "tot_object_list": queryset_list,
        "share_string": share_string,
        "comments": comments,
        "comment_form":form,
        "aggr_data":pagedata,
        }
    return render(request, "post_detail.html", context)

def post_list(request):
    posts,pagedata=init()
    today = timezone.now().date()
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = custom_paging(queryset_list,page)
    context = {
        "object_list": queryset,
        "tot_object_list": queryset_list,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
        "aggr_data":pagedata,
        }

    return render(request, "post_list.html", context)

def custom_paging(queryset_list,page):
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page = page
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
		# If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    return queryset


def post_update(request,year=None,month=None,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,publish__year=int(year), publish__month=int(month),slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Post Saved Successfully", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request,year=None,month=None, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,publish__year=int(year), publish__month=int(month),slug=slug)
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("posts:list")

# new code #
MONTH_NAMES = ('', 'January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December')

def init():
    posts = Post.objects.active()
    tag_data = create_tag_data(posts)
    archive_data = create_archive_data(posts)
    pagedata = {'version': '0.0.5',
                'post_list': posts,
                'tag_counts': tag_data,
                'archive_counts': archive_data,}
    return posts, pagedata

def create_archive_data(posts):
    archive_data = []
    count = {}
    mcount = {}
    for post in posts:
        year = post.publish.year
        month = post.publish.month
        if year not in count:
            count[year] = 1
            mcount[year] = {}
        else:
            count[year] += 1
        if month not in mcount[year]:
            mcount[year][month] = 1
        else:
            mcount[year][month] += 1
    for year in sorted(count.iterkeys(), reverse=True):
        archive_data.append({'isyear': True,
                             'year': year,
                             'count': count[year],})
        for month in sorted(mcount[year].iterkeys(), reverse=True):
            archive_data.append({'isyear': False,
                                 'yearmonth': '%d/%02d' % (year, month),
                                 'monthname': MONTH_NAMES[month],
                                 'count': mcount[year][month],})
    return archive_data

def create_tag_data(posts):
    tag_data = []
    count = {}
    for post in posts:
        tags = re.split(" ", post.tags)
        for tag in tags:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1
    for tag, count in sorted(count.iteritems(), key=lambda(k, v): (v, k), reverse=True):
        tag_data.append({'tag': tag,
                         'count': count,})
    return tag_data

def frontpage(request):
    posts, pagedata = init()
    pagedata.update({'subtitle': '',})
    #return render_to_response('listpage.html', pagedata)
    return render(request,'listpage.html', pagedata)

def singlepost(request, year, month, slug2):
    posts, pagedata = init()
    post = posts.get(timestamp__year=year,
                            timestamp__month=int(month),
                            slug=slug2,)
    pagedata.update({'post': post})
    #return render_to_response('singlepost.html', pagedata)
    return render(request,'singlepost.html', pagedata)

def yearview(request, year):
    posts, pagedata = init()
    tot_posts = posts
    posts = posts.filter(publish__year=year)
    pagedata.update({'post_list': posts,
                     'subtitle': 'Posts for %s' % year})
    today = timezone.now().date()
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = custom_paging(tot_posts,page)
    context = {
        "object_list": posts,
        "tot_object_list": tot_posts,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
        "aggr_data":pagedata,
        }

    return render(request, "post_list.html", context)

def monthview(request, year, month):
    posts, pagedata = init()
    tot_posts = posts
    posts = posts.filter(publish__year=year)
    posts = posts.filter(publish__month=int(month))
    pagedata.update({'post_list': posts,
                     'subtitle': 'Posts for %s %s' % (MONTH_NAMES[int(month)], year),})
    today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": tot_posts,
        "title": "List",
        #"page_request_var": page_request_var,
        "today": today,
        "aggr_data":pagedata,
        }
    return render(request, "post_list.html", context)

def tagview(request, tag):
    allposts, pagedata = init()
    posts = []
    for post in allposts:
        tags = re.split(' ', post.tags)
        if tag in tags:
            posts.append(post)
    pagedata.update({'post_list': posts,
                     'subtitle': "Posts tagged '%s'" % tag,})
    today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": allposts,
        "title": "List",
        #"page_request_var": page_request_var,
        "today": today,
        "aggr_data":pagedata,
        }
    return render(request, "post_list.html", context)
