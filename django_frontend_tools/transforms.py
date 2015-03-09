import os
import hashlib
from django_node import npm
from .services import CompressCSSService, AutoprefixerService, LessService, CompressJSService

# Temp fix so that the services are only installed once
# TODO: fix in django-node and backport
npm.install(os.path.dirname(__file__))

autoprefixer_service = AutoprefixerService()
less_service = LessService()
compress_css_service = CompressCSSService()
compress_js_service = CompressJSService()


def transform_name_to_css(file_name, content):
    path_to_file, ext = os.path.splitext(file_name)
    return path_to_file + '.css'


def autoprefixer(css, options=None):
    return autoprefixer_service.autoprefix(css, options)


def less(path_to_file, options=None):
    return less_service.compile(path_to_file, options)
less.file_name_transform = transform_name_to_css


def compress_css(css=None, path_to_file=None, options=None):
    return compress_css_service.compress(css, path_to_file, options)


def compress_js(js=None, path_to_file=None, options=None):
    return compress_js_service.compress(js, path_to_file, options)


def version_file_name(file_name, content):
    path_to_file, ext = os.path.splitext(file_name)
    md5 = hashlib.md5()
    md5.update(content)
    return path_to_file + '-' + md5.hexdigest() + ext


# def rewrite_css_urls(css, path_to_file=None, prepend=None):
#