import os
from django.conf import settings
from compressor.filters import FilterBase
from .transforms import compress_css, compress_js


class CompressCSSFilter(FilterBase):
    def input(self, **kwargs):
        filename = kwargs.get('filename', None)
        if filename:
            prepend_to_relative_urls = None
            if kwargs.get('basename', None):
                # Rewrite relative urls to absolute urls
                prepend_to_relative_urls = settings.STATIC_URL + os.path.dirname(kwargs['basename']) + '/'
            return compress_css(path_to_file=filename, prepend_to_relative_urls=prepend_to_relative_urls)
        return compress_css(kwargs['elem']['text'])

    def output(self, **kwargs):
        raise NotImplementedError


class CompressJSFilter(FilterBase):
    def input(self, **kwargs):
        filename = kwargs.get('filename', None)
        if filename:
            return compress_js(path_to_file=filename)
        return compress_js(kwargs['elem']['text'])

    def output(self, **kwargs):
        raise NotImplementedError