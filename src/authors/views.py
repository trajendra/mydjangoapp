try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from .forms import ProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Profile

import re

def profile_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Profile, slug=slug)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Profile Saved Successfully", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, "profile_form.html", context)

def profile_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Profile, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("profile:profile")

def profile_view(request,slug):
    instance = get_object_or_404(Profile,slug=slug)
    share_string = quote_plus(instance.profile)
    profiles, pagedata = init()
    queryset_list = Profile.objects.all().order_by("-height_field")

    #if request.user.is_staff or request.user.is_superuser:
     #   queryset_list = Profile.objects.all()

    context = {
        "instance": instance,
        "tot_object_list": queryset_list,
        "share_string": share_string,
        "aggr_data": pagedata,
    }
    return render(request, "profile_view.html", context)

def about_us(request):
    profiles,pagedata = init()
    context = {
        "profiles": profiles,
        "aggr_data": pagedata,
    }
    return render(request, "about.html", context)

def init():
    profiles = Profile.objects.all().order_by("-height_field")
    #skills = create_skill_data(profiles)
    pagedata = {'version': '1',
                'profile_list': profiles,
                #'skill_counts': skills,
                }
    return profiles, pagedata

def create_skill_data(profiles):
    skill_data = []
    count = {}
    for prof in profiles:
        skills = re.split(" ", prof.skills)
        for skill in skills:
            if skill not in count:
                count[skill] = 1
            else:
                count[skill] += 1
    for skill, count in sorted(count.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        skill_data.append({'skill': skill,
                         'count': count,})
    return skill_data