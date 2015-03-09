import os
import sys
import json
from django.utils import six
from django_node.base_service import BaseService
from django_node.exceptions import NodeServiceError
from ..exceptions import (
    MissingArgumentError, AutoprefixerError, LessCompileError, CSSCompressionError, JSCompressionError
)


class AutoprefixerService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'autoprefixer.js')

    def autoprefix(self, css, options=None):
        params = {
            'css': css
        }

        if options is not None:
            params['options'] = json.dumps(options)

        try:
            response = self.send(**params)
        except NodeServiceError as e:
            six.reraise(AutoprefixerError, AutoprefixerError(*e.args), sys.exc_info()[2])

        return response.text


class LessService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'less.js')

    def compile(self, path_to_file, options=None):
        params = {
            'path_to_file': path_to_file
        }

        if options is not None:
            params['options'] = json.dumps(options)

        try:
            response = self.send(**params)
        except NodeServiceError as e:
            six.reraise(LessCompileError, LessCompileError(*e.args), sys.exc_info()[2])

        return response.text


class CompressCSSService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'compress_css.js')

    def compress(self, css, path_to_file=None, options=None):
        params = {}

        if css is not None:
            params['css'] = css
        elif path_to_file is not None:
            params['path_to_file'] = path_to_file
        else:
            raise MissingArgumentError('compress_css requires either `css` or `path_to_file` arguments to be defined')

        if options is not None:
            params['options'] = json.dumps(options)

        try:
            response = self.send(**params)
        except NodeServiceError as e:
            six.reraise(CSSCompressionError, CSSCompressionError(*e.args), sys.exc_info()[2])

        return response.text


class CompressJSService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'compress_js.js')

    def compress(self, js, path_to_file=None, options=None):
        params = {}

        if js is not None:
            params['js'] = js
        elif path_to_file is not None:
            params['path_to_file'] = path_to_file
        else:
            raise MissingArgumentError('compress_js requires either `js` or `path_to_file` arguments to be defined')

        if options is not None:
            params['options'] = json.dumps(options)

        try:
            response = self.send(**params)
        except NodeServiceError as e:
            six.reraise(JSCompressionError, JSCompressionError(*e.args), sys.exc_info()[2])

        return response.text