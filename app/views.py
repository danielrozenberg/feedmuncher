from datetime import timedelta
import re

from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.shortcuts import render_to_response
from django.utils import timezone
from django.utils.translation import ugettext as _

from app.helpers import generate_failed_feed, render_feed_preview, munch_feed, update_munched_feed
from app.models import MunchedFeed, MunchedFeedForm


@login_required
def list_feeds(request):
    munched_feeds = MunchedFeed.objects.filter(user=request.user)

    return render(request, 'app/list.html', context={
        'munched_feeds': munched_feeds
    })


@login_required
def new_feed(request):
    if request.method == 'POST':
        post = request.POST.dict()
        post.update({'user': request.user.id})
        form = MunchedFeedForm(post)

        if form.is_valid():
            munched_feed = form.save()
            return redirect('update_feed', slug=munched_feed.slug)
    else:
        form = MunchedFeedForm()

    return render(request, 'app/edit.html', context={
        'form': form
    })


@login_required
def edit_feed(request, slug):
    munched_feed = get_object_or_404(MunchedFeed, user=request.user, slug=slug)

    if request.method == 'POST':
        post = request.POST.dict()
        post.update({'user': request.user.id})
        form = MunchedFeedForm(post, instance=munched_feed)

        if form.is_valid():
            munched_feed = form.save()
            return redirect('update_feed', slug=munched_feed.slug)
    else:
        form = MunchedFeedForm(instance=munched_feed)

    return render(request, 'app/edit.html', context={
        'form': form,
        'munched_feed': munched_feed,
        'slug': slug
    })


@login_required
def preview_feed(request):
    now = timezone.now()
    current_url = request.build_absolute_uri()
    source_url = request.GET['source_url']

    try:
        extract_css_selector = request.GET.get('extract_css_selector', None) or 'body'
        title_regex = re.compile(request.GET.get('title_regex', None) or r'^.?')
        content_regex = re.compile(request.GET.get('content_regex', None) or r'^.?')
        ignore_bozo = bool(request.GET.get('ignore_bozo', False))

        output_feed = munch_feed(current_url, source_url, extract_css_selector, title_regex, content_regex, ignore_bozo)

        return render_feed_preview(output_feed)
    except Exception as e:
        failed_feed = generate_failed_feed(e, current_url, source_url, now)
        return render_feed_preview(failed_feed)


@login_required
def update_feed(request, slug):
    munched_feed = get_object_or_404(MunchedFeed, user=request.user, slug=slug)

    return render_to_response('app/update.html', context={
        'munched_feed': munched_feed
    })


@login_required
def really_update_feed(request, slug):
    munched_feed = get_object_or_404(MunchedFeed, user=request.user, slug=slug)

    if update_munched_feed(munched_feed):
        messages.success(request,
                         _('The feed %(munched_feed)s was successfully updated.') % {'munched_feed': munched_feed})
    else:
        messages.error(request,
                       _('There was an error updating the feed %(munched_feed)s. '
                         '<a href="%(edit_url)s">Edit</a> this feed to fix the error.') % {
                           'munched_feed': munched_feed, 'edit_url': resolve_url('edit_feed', slug=munched_feed.slug)})

    return redirect('list_feeds')


@login_required
def delete_feed(request, slug):
    munched_feed = get_object_or_404(MunchedFeed, user=request.user, slug=slug)

    if request.method == 'POST':
        munched_feed.delete()
        messages.info(request, _('Deleted the feed %(munched_feed)s.') % {'munched_feed': munched_feed})
        return redirect('list_feeds')

    return render(request, 'app/delete.html', context={
        'munched_feed': munched_feed
    })


def serve_feed(request, user, slug):
    munched_feed = get_object_or_404(MunchedFeed, user__username=user, slug=slug)

    if munched_feed.last_updated:
        response = HttpResponse(content_type=munched_feed.cache_mime_type)
        response.write(munched_feed.cache)

        return response
    else:
        now = timezone.now()
        failed_feed = generate_failed_feed(Exception(_('This feed has not been munched yet!')),
                                           munched_feed.build_absolute_uri(), munched_feed.source_url, now)
        return render_feed_preview(failed_feed)


def mass_update(request):
    now = timezone.now()
    now_minus_interval = now - timedelta(seconds=settings.FEED_MUNCHER_UPDATE_INTERVAL)
    max_feeds = settings.FEED_MUNCHER_MAX_FEEDS

    munched_feeds = MunchedFeed.objects.filter(
        Q(last_updated__lt=now_minus_interval) | Q(last_updated__isnull=True)).order_by('last_updated')[0:max_feeds]
    for munched_feed in munched_feeds:
        update_munched_feed(munched_feed)

    return HttpResponse(content_type='text/plain',
                        content=_('Updated %(count)d feeds.' % {'count': len(munched_feeds)}))
