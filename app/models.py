from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.forms import HiddenInput
from django.shortcuts import resolve_url
from django.utils.translation import gettext as _


class MunchedFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    source_url = models.URLField()
    extract_css_selector = models.CharField(max_length=255, blank=True)
    title_regex = models.CharField(max_length=255, blank=True)
    content_regex = models.CharField(max_length=255, blank=True)
    ignore_bozo = models.BooleanField(default=False)

    last_updated = models.DateTimeField(null=True, blank=True)
    cache = models.TextField(null=True, blank=True)
    cache_mime_type = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'slug')

    def __str__(self):
        return self.slug

    def build_absolute_uri(self):
        return resolve_url('serve_feed', user=self.user, slug=self.slug)


class MunchedFeedForm(forms.ModelForm):
    class Meta:
        model = MunchedFeed
        fields = ['user', 'slug', 'source_url', 'extract_css_selector', 'title_regex', 'content_regex', 'ignore_bozo']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('You already have a munched feed with that name.')
            }
        }
