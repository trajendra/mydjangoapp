try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from .forms import ProfileForm,ContactForm
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Profile
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.core.mail import send_mail

import re

def profile_update(request, slug=None):
    #if not (request.user.is_staff or request.user.is_superuser):
    #    raise Http404
    instance = get_object_or_404(Profile,user=request.user, slug=slug)
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
    if not request.user.is_staff or request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Profile, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("profile:profile")

def profile_view(request,slug=None):
    #if not request.user.is_authenticated:
    #profile = get_object_or_404(Profile, slug=slug)
    if not slug:
        if request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(
            user=request.user,)
    else:
        profile = get_object_or_404(Profile, slug=slug)
    context = {
        "instance": profile,
    }
    return render(request, "profile_view.html", context)

def authors_view(request):
    users = User.objects.all().filter(is_staff=1)
    profiles = Profile.objects.all().filter( user_id__in= users)
    context = {
        "profiles": profiles,
    }
    return render(request, "about.html", context)

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

def contact_view(request):
    title="Contact"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        user_email = form.cleaned_data['sender']
        message = '\n'+ message + '\n\n Recieved on behalf of user : '+user_email + '\n \n Best Regards,\n Xchangeidea.Net'
        sender = 'Hello <admin@xchangeidea.net>'
        cc_myself = form.cleaned_data['cc_myself']
        recipients = ['raj@xchangeidea.net']
        if cc_myself:
            recipients.append(user_email)

        send_mail(subject, message, sender, recipients)
        messages.success(request, "Thank you for contacting us, we have received your email!!")
        return redirect('/contact/')

    context = {
        "form": form,
        "title": title
    }
    return render(request,"contact.html", context)