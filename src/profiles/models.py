from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

# Create your models here.

def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    first_name = models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    email = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0,blank=True,null=True)
    width_field = models.IntegerField(default=0,blank=True,null=True)
    profile = RichTextUploadingField(null=True,blank=True)
    skills = models.CharField(max_length=4000,null=True, blank=True)
    learn_interests = models.CharField(max_length=4000,null=True, blank=True)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse("profiles:pview", kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.user)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Profile)
