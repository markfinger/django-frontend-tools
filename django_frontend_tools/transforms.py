import os
from .services import CompressCSSService, AutoprefixerService, LessService, CompressJSService
from .utils import change_file_ext_to_css


autoprefixer_service = AutoprefixerService()
less_service = LessService()
compress_css_service = CompressCSSService()
compress_js_service = CompressJSService()


def autoprefixer(css, options=None):
    return autoprefixer_service.autoprefix(css, options)


def less(path_to_file, options=None):
    return less_service.compile(path_to_file, options)
less.file_name_transform = change_file_ext_to_css


def compress_css(css=None, path_to_file=None, options=None, prepend_to_relative_urls=None):
    return compress_css_service.compress(css, path_to_file, options, prepend_to_relative_urls)


def compress_js(js=None, path_to_file=None, options=None):
    return compress_js_service.compress(js, path_to_file, options)
