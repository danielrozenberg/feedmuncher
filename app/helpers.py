from datetime import datetime
import re
from time import mktime

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.utils import timezone
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext as _
import feedparser
import requests


def munch_feed(munched_feed_url, source_feed_url, extract_css_selector, title_regex, content_regex, ignore_bozo):
    source_feed = feedparser.parse(source_feed_url)
    if source_feed.bozo and not ignore_bozo:
        raise Exception(_('Origin feed %(source_url)s is malformed. Error found: %(exception)r.' % {
            'source_url': source_feed_url,
            'exception': source_feed.bozo_exception
        }))
    output_feed = _convert_feed(source_feed['feed'], munched_feed_url)
    for input_entry in source_feed['items']:
        if not title_regex.search(input_entry['title']):
            continue

        response = requests.get(input_entry['link'])
        raw_html = response.text
        if not content_regex.search(raw_html):
            continue

        _add_converted_item(output_feed, input_entry, raw_html, extract_css_selector)
    return output_feed


def generate_failed_feed(e, munched_feed_url, source_feed_url, now):
    failed_feed = Atom1Feed(title=_('Error in Feed Muncher'),
                            link=munched_feed_url,
                            description=_('There was an error while munching this feed.'),
                            subtitle=_('Feed Muncher'))
    failed_feed.add_item(title='Error in Feed Muncher',
                         link=munched_feed_url,
                         description=_('There was an error processing your feed in Feed Muncher. '
                                       'An exception was thrown. %(exception)r' % {'exception': e}),
                         author_name=_('Feed Muncher'),
                         pubdate=now,
                         unique_id=source_feed_url + ':error',
                         unique_id_is_permalink=False,
                         updateddate=now)
    return failed_feed


def render_feed_preview(feed):
    response = HttpResponse(content_type=feed.content_type)
    feed.write(response, 'utf-8')
    return response


def update_munched_feed(munched_feed):
    now = timezone.now()
    try:
        output_feed = munch_feed(munched_feed.build_absolute_uri(), munched_feed.source_url,
                                 munched_feed.extract_css_selector, re.compile(munched_feed.title_regex),
                                 re.compile(munched_feed.content_regex), munched_feed.ignore_bozo)

        munched_feed.last_updated = now
        munched_feed.cache = output_feed.writeString('utf-8')
        munched_feed.cache_mime_type = output_feed.content_type
        munched_feed.save()
        return True

    except Exception as e:
        failed_feed = generate_failed_feed(e, munched_feed.build_absolute_uri(), munched_feed.source_url, now)

        munched_feed.last_updated = now
        munched_feed.cache = failed_feed.writeString('utf-8')
        munched_feed.cache_mime_type = failed_feed.content_type
        return False


def _convert_feed(input_feed, current_url):
    # TODO more params?
    return Atom1Feed(title=input_feed['title'],
                     link=input_feed['link'],
                     description=_try_extract(input_feed['description']) or _try_extract(input_feed['subtitle']),
                     language=_try_extract(input_feed, 'language'),
                     subtitle=(_try_extract(input_feed, 'subtitle') + _(' // via Feed Muncher')).strip(),
                     feed_url=current_url,
                     feed_copyright=_try_extract(input_feed, 'rights'))


def _add_converted_item(output_feed, input_entry, raw_html, extract_css_selector):
    html = BeautifulSoup(raw_html, 'html.parser')
    description = ''
    for sub_selector in extract_css_selector.split(','):
        selections = html.select(sub_selector)
        if selections:
            description += '<div>%s</div>' % '</div> <div>'.join((str(selection) for selection in selections))
    if not description:
        description = _try_extract(input_entry, 'summary') or _try_extract(input_entry, 'description')
    unique_id = _try_extract(input_entry, 'id') or input_entry['link']

    output_feed.add_item(title=input_entry['title'],
                         link=input_entry['link'],
                         description=description,
                         author_name=_try_extract(input_entry, 'author'),
                         pubdate=_time_struct_to_datetime(_try_extract(input_entry, 'published_parsed')),
                         unique_id=unique_id,
                         unique_id_is_permalink=unique_id.startswith('http'),
                         updated=_time_struct_to_datetime(_try_extract(input_entry, 'updated_parsed')))


def _time_struct_to_datetime(time_struct):
    if time_struct:
        return datetime.fromtimestamp(mktime(time_struct))
    return None


def _try_extract(d, *fields):
    while fields:
        next_field = fields[0]
        if next_field in d:
            d = d[next_field]
            fields = fields[1:]
        else:
            return None
    return d
