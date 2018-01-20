# class SimpleMiddleware(object):
#     # def __init__(self, get_response):
#     #     self.get_response = get_response
#         # One-time configuration and initialization.

#     # def __call__(self, request):
#     #     # Code to be executed for each request before
#     #     # the view (and later middleware) are called.

#     #     response = self.get_response(request)
#     #     print 'Hello World'

#     #     # Code to be executed for each request/response after
#     #     # the view is called.

#     #     return response
#     def process_exception(self, request, exception):
#         if settings.DEBUG:
#             print exception.__class__.__name__
#             print exception.message
#             print 'Hello World'
#         return None
import requests
import urllib
from django.conf import settings

class SimpleMiddleware(object):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            intitle = u'{}: {}'.format(exception.__class__.__name__,  exception.message)
            print intitle

            url = 'https://api.stackexchange.com/2.2/search'
            headers = { 'User-Agent': 'github.com/vitorfs/seot' }
            params = {
                'order': 'desc',
                'sort': 'votes',
                'site': 'stackoverflow',
                'pagesize': 3,
                'tagged': 'python;django',
                'intitle': intitle
            }

            r = requests.get(url, params=params, headers=headers)
            questions = r.json()

            print ''

            for question in questions['items']:
                print question['title']
                print question['link']
                print ''

        return None