try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import MessageForm
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView

from .forms import PostForm
from .models import Post,Category,SubCategory
from profiles.models import Profile
from comments.forms import CommentForm
from comments.models import Comment

import models
import json as simplejson
import re

def get_subcategory(request, ctg_id):
    ctg = models.Category.objects.get(pk=ctg_id)
    subctgs = models.SubCategory.objects.filter(category=ctg)
    subctg_dict = {}
    for sc in subctgs:
        subctg_dict[sc.id] = sc.name
    return HttpResponse(simplejson.dumps(subctg_dict), content_type="application/json")

def post_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug, year, month):
    instance = get_object_or_404(Post, publish__year=int(year), publish__month=int(month), slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    post_id = instance.pk

    if not request.session.get(str(post_id),False):
        request.session[post_id] = True
        instance.views = instance.views+1
        instance.save()

    liked = False
    if request.session.get('has_liked_' + str(post_id), liked):
        liked = True
        #messages.info(request,"liked {}_{}".format(liked, post_id))

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
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        subject = ' Comment recieved - " ' + instance.title[0:50] + '.. ."'
        message = ' Post Title : ' + instance.title + '. \n Comment : ' + str(content_data) + '. \n User : ' + str(
            request.user)
        sender = 'XChange Idea <admin@xchangeidea.net>'
        recipients = ['mail2raajj@gmail.com']
        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    queryset_list, pagedata = init()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")

    queryset_list = queryset_list.only('title')
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "tot_object_list": queryset_list,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
        "aggr_data": pagedata,
        'liked': liked,
    }
    return render(request, "post_detail.html", context)

def like_count_blog(request):
    liked = False
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))
        if request.session.get('has_liked_'+post_id, liked):
            print("unlike")
            if post.likes > 0:
                likes = post.likes - 1
                try:
                    del request.session['has_liked_'+post_id]
                except KeyError:
                    print("keyerror")
        else:
            print("like")
            request.session['has_liked_'+post_id] = True
            likes = post.likes + 1
    post.likes = likes
    post.save()
    return HttpResponse(likes, liked)

def post_list(request):
    queryset_list, pagedata = init()
    today = timezone.now().date()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = custom_paging(queryset_list, page)
    context = {
        "object_list": queryset,
        "tot_object_list": queryset_list,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
        "aggr_data": pagedata,
    }

    return render(request, "post_list.html", context)

def custom_paging(queryset_list, page):
    paginator = Paginator(queryset_list, 15)  # Show 15 contacts per page
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

def post_update(request, year=None, month=None, slug=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instance = get_object_or_404(Post,user=request.user, publish__year=int(year), publish__month=int(month), slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Saved Successfully", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, year=None, month=None, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, publish__year=int(year), publish__month=int(month), slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")

# new code #
MONTH_NAMES = ('', 'January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December')

def init():
    posts = Post.objects.active().order_by("-timestamp")
    tag_data = create_tag_data(posts)
    archive_data = create_archive_data(posts)
    category_data = create_ctg_data(posts)
    pagedata = {'tag_counts': tag_data,
                'archive_counts': archive_data,
                'ctg_counts' :category_data,}
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

        tags = re.split(",", post.tags.replace(" ",""))

        for tag in tags:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1
    for tag, count in sorted(count.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        tag_data.append({'tag': tag,
                         'count': count,})
    return tag_data

def create_ctg_data(posts):
    ctg_data = []
    ccount = {}
    sccount = {}
    for post in posts:
        ctg = post.category
        subctg = post.subcategory
        if ctg not in ccount:
            ccount[ctg] = 1
            sccount[ctg] = {}
        else:
            ccount[ctg] += 1
        if subctg not in sccount[ctg]:
            sccount[ctg][subctg] = 1
        else:
            sccount[ctg][subctg] += 1
    for ctg in (ccount.iterkeys()):
        ctg_data.append({ 'ctg': ctg,'ccount': ccount[ctg],'isctg': True,})
        for subctg in (sccount[ctg].iterkeys()):
            ctg_data.append({'ctg': ctg,'subctg':subctg,
                                 'ctgsc': '%s/%s' % (ctg, subctg),
                                 'sccount': sccount[ctg][subctg],'isctg': False,})

    return ctg_data

def ctgview(request, ctg,subctg=None):
    posts, pagedata = init()

    if request.user.is_staff or request.user.is_superuser:
        posts = Post.objects.all().order_by("-timestamp")


    if ctg:
        ctg=Category.objects.filter(name=ctg)
    if subctg:
        subctg=SubCategory.objects.filter(category_id__in=ctg,name=subctg)
        posts = posts.filter(category_id__in=ctg,subcategory_id__in=subctg)
    if not subctg:
        posts = posts.filter(category_id__in=ctg)

    tot_posts = posts.only('title')
    #pagedata.update({'post_list': posts,
    #                 'subtitle': 'Posts for %s' %subctg})
    #today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": tot_posts,
        "aggr_data": pagedata,
    }

    return render(request, "post_list.html", context)

def yearview(request, year):
    posts, pagedata = init()
    tot_posts = posts
    posts = posts.filter(publish__year=year)
    pagedata.update({'post_list': posts,
                     'subtitle': 'Posts for %s' % year})
    today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": tot_posts,
        "title": "List",
        "today": today,
        "aggr_data": pagedata,
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
        # "page_request_var": page_request_var,
        "today": today,
        "aggr_data": pagedata,
    }
    return render(request, "post_list.html", context)

def tagview(request, tag):
    allposts, pagedata = init()
    posts = []
    for post in allposts:
        tags = re.split(",", post.tags.replace(" ",""))
        if tag in tags:
            posts.append(post)
    pagedata.update({'post_list': posts,
                     'subtitle': "Posts tagged '%s'" % tag,})
    today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": allposts,
        "title": "List",
        # "page_request_var": page_request_var,
        "today": today,
        "aggr_data": pagedata,
    }
    return render(request, "post_list.html", context)

def userview(request, slug=None):
    posts, pagedata = init()
    if slug:
        profile = get_object_or_404(Profile, slug=slug)
        posts = Post.objects.all().filter(user=profile.user)
    else:
        if request.user.is_authenticated:
            posts = posts.filter(user_id=request.user)

    tot_posts = posts.only('title')
    #pagedata.update({'post_list': posts,
    #                 'subtitle': 'Posts for %s' %subctg})
    #today = timezone.now().date()
    context = {
        "object_list": posts,
        "tot_object_list": tot_posts,
        "aggr_data": pagedata,
    }

    return render(request, "post_list.html", context)