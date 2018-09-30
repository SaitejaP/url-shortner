# import hashlib
import random
# from base64 import b64encode
from urllib.parse import urlparse, urlunparse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from url_shortner.utils import get_response

from . import constants
from .models import URLDetails, URLMapper


class URLsListView(View):

    def get(self, request, *args, **kwargs):
        try:
            data = {}
            data['url_maps'] = [item.serializer() for item in URLMapper.objects.all()]
            data['count'] = len(data['url_maps'])
            message = 'Urls fetched successfully'
            response = get_response(constants.API_SUCCESS, data, message)
            return JsonResponse(response)
        except Exception:
            response = get_response(constants.API_FAILED, None, constants.GENERIC_ERROR_MSG)
            return JsonResponse(status=500, data=response)


@method_decorator(csrf_exempt, name='dispatch')
class ShortenUrlView(View):

    default_scheme = 'https'

    def validate(self, data):
        long_url = data.get('long_url')
        if not long_url:
            raise ValidationError('Url is required')

        long_url = self.pre_process_url(long_url)

        URLValidator()(long_url)

        self.long_url = long_url

    def pre_process_url(self, old_url):
        '''
        preprocess urls
        adds missing sheme & fixes path and netloc
        '''
        scheme, netloc, path, params, query, fragment = urlparse(old_url)
        if not netloc:
            if not path.startswith('www'):
                netloc = '%s.%s' % ('www', path)
            else:
                netloc = path.split('/')[0]
            path = '/'.join(path.split('/')[1:])
        elif not netloc.startswith('www'):
            netloc = '%s.%s' % ('www', netloc)

        return urlunparse((self.default_scheme, netloc, path, params, query, fragment))

    def shorten_url(self):
        # return hashlib.md5(long_url.encode()).digest().b64encode()
        return ''.join(random.choice('0123456789ABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz_-') for i in range(6))

    def post(self, request, *args, **kwargs):
        try:
            self.validate(request.POST)
        except ValidationError as e:
            response = get_response(constants.API_FAILED, None, str(e))
            return JsonResponse(status=400, data=response)

        repeat = True
        while repeat:
            short_url = self.shorten_url()
            url_mapper, is_created = URLMapper.objects.get_or_create(
                long_url=self.long_url, defaults={
                    'short_url': short_url
                }
            )
            if not is_created and url_mapper.long_url != self.long_url:
                continue
            repeat = False

        message = 'URL shortened successfully'
        response = get_response(constants.API_SUCCESS, url_mapper.serializer(), message)
        return JsonResponse(response)

class RedirectView(View):

    def get(self, request, *args, **kwargs):
        path = kwargs.get('path')
        try:
            url_mapping = URLMapper.objects.get(short_url=path)
            URLDetails.objects.create(url_mapping=url_mapping)
        except URLMapper.DoesNotExist:
            return JsonResponse(status=404, data=None)

        return HttpResponseRedirect(url_mapping.long_url)
