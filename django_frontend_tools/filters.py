import os
from django.conf import settings
from compressor.filters import FilterBase
from .transforms import compress_css, compress_js


class CompressCSSFilter(FilterBase):
    def input(self, **kwargs):
        filename = kwargs.get('filename', None)
        if filename:
            options = {}
            if kwargs.get('basename', None):
                basedir = os.path.dirname(kwargs['basename'])
                options['relativeTo'] = settings.STATIC_URL + basedir
                options['target'] = (settings.COMPRESS_URL + settings.COMPRESS_OUTPUT_DIR + '/css/' + basedir)
            return compress_css(path_to_file=filename, options=options)
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