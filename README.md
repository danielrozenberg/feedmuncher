Feed Muncher
============

Manipulate existing feeds by filtering and extracting parts of the full content.

Feed Muncher takes an existing input feed, filters each entry's title against a regex, pulls the full HTML content by
loading the content's URL, filters against another regex, and extracts selected parts via a CSS selector.

Some knowledge of [Regular Expressions](http://regexone.com/) and [CSS selectors](http://flukeout.github.io/) required
(knowledge of CSS rules not required.)


Deploying Feed Muncher
----------------------

1. [Create a virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with Python 2.7.x and
`requirements.txt` (or install the requirements in your own environment)
2. Copy `feed_muncher/example_settings.py` to `feed_muncher/settings.py` and modify settings to fit your environment.
See [Django settings](https://docs.djangoproject.com/en/1.8/topics/settings/) for instructions.
3. Activate the virtualenv (usually `source /path/to/venv/bin/activate`), then create the database and first user by
running the command `python manage.py migrate` and `python manage.py createsuperuser`.
4. Run the app on your server using [whichever method works
best](https://docs.djangoproject.com/en/1.8/howto/deployment/) for your case. DreamHost has a [simple
tutorial](http://wiki.dreamhost.com/Django) for shared hosting.
5. Set a cron job to `curl http://your.deployment.example.com/feed/mass-update` (or `wget` or any other fetching tool)
to automatically update the feeds. The following variables inside `settings.py` affect the mass updater:
 * `FEED_MUNCHER_UPDATE_INTERVAL` = A feed will only be updated if this number of seconds have passed since it was
 last updated
 * `FEED_MUNCHER_MAX_FEEDS` = Up to this number of feeds will be updated in one execution of `/feed/mass-update`.


Deploying locally
-----------------

You can test the app locally by following the steps 1–3 above and running `python manage.py serve`. The server will
run on `http://localhost:8000/`.
