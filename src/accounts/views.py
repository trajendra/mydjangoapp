from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import UserLoginForm, UserRegisterForm, ContactForm

def login_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "login.html", {"form":form, "title": title})


def register_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)

        subject = ' Welcome to Xchange Idea Network .. '
        message = ' Hi ' + str(user.username) + ' \n\n Thank you for registering with us \n\n Please confirm your email id by clicking on the below url '
        sender = 'XChangeIdea.Net <e@mail.xchangeidea.net>'
        recipients = [user.email]
        send_mail(subject, message, sender, recipients)

        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")

def contact_view(request):
    title="Contact"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']

        recipients = ['mail2raajj@gmail.com']
        if cc_myself:
            recipients.append(sender)

        send_mail(subject, message, sender, recipients)
        messages.success(request, "Thank you for contacting us, we have received your email!!")
        return redirect('/contact/')

    context = {
        "form": form,
        "title": title
    }
    return render(request,"contact.html", context)
