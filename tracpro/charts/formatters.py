from __future__ import unicode_literals

from smartmin.views import smart_url


def format_series(pollruns, data, url=None, **extra):
    """Format a series of data. A point will be created for each pollrun.

    If a url is provided, each point will be a link.
    """
    def format_point(pollrun):
        point = {'y': data.get(pollrun.pk, 0)}
        if url:
            point['url'] = smart_url(url, pollrun)
        return point

    extra['data'] = [format_point(pollrun) for pollrun in pollruns]
    return extra


def format_x_axis(pollruns):
    return [pollrun.conducted_on.strftime('%Y-%m-%d') for pollrun in pollruns]