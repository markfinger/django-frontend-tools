import os
import unittest
from django.conf import settings
from django.template import Template, Context
from django_frontend_tools.transforms import autoprefixer, less, compress_css, compress_js

TEST_LESS_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'test.less')
TEST_AUTOPREFIXER_LESS_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'autoprefixer-test.less')
TEST_CSS_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'test.css')
TEST_JS_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'test.js')
BOOTSTRAP_CSS_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'bootstrap.css')
BOOTSTRAP_CSS_EXPECTED_OUTPUT_FILE = os.path.join(settings.BASE_DIR, 'test_static', 'bootstrap.min.css')


class TestDjangoFrontendTools(unittest.TestCase):
    def test_autoprefix_css_can_process_css_string(self):
        css = '.foo { -webkit-border-radius: 100%; border-radius: 100%; }'
        expected = '.foo { border-radius: 100%; }'
        self.assertEqual(autoprefixer(css), expected)

    def test_can_compile_less_file(self):
        expected = 'body {\n  color: blue;\n}\nbody .foo {\n  color: pink;\n}\n#foo .bar {\n  color: red;\n}\n'
        self.assertEqual(less(TEST_LESS_FILE), expected)

    def test_compress_css_can_compress_file(self):
        expected = 'body{color:#00f}#foo .bar{color:red}'
        self.assertEqual(compress_css(path_to_file=TEST_CSS_FILE), expected)

    def test_compress_css_can_compress_css_string(self):
        css = '''
        body {
            color: blue;
        }

        #foo .bar {
            color: red;
        }
        '''
        expected = 'body{color:#00f}#foo .bar{color:red}'
        self.assertEqual(compress_css(css), expected)

    def test_compress_js_can_compress_file(self):
        expected = 'var foo="bar",bar=function(){return foo};module.exports=bar;'
        self.assertEqual(compress_js(path_to_file=TEST_JS_FILE), expected)

    def test_compress_js_can_compress_js_string(self):
        js = '''
        var foo = 'bar';

        var bar = function() {
            return foo;
        };

        module.exports = bar;
        '''
        expected = 'var foo="bar",bar=function(){return foo};module.exports=bar;'
        self.assertEqual(compress_js(js), expected)

    def test_can_pipe_less_output_to_autoprefixer(self):
        expected = 'body {\n  color: blue;\n}\nbody .foo {\n  color: pink;\n}\n#foo {\n  border-radius: 100%;\n}\n'
        self.assertEqual(autoprefixer(less(TEST_AUTOPREFIXER_LESS_FILE)), expected)

    def test_can_pipe_less_output_to_autoprefixer_to_compress_css(self):
        expected = 'body{color:#00f}body .foo{color:pink}#foo{border-radius:100%}'
        self.assertEqual(compress_css(autoprefixer(less(TEST_AUTOPREFIXER_LESS_FILE))), expected)

    def test_can_compile_less_file_from_template_tag(self):
        template = Template('{% load frontend_tools %}{% frontend_tools less \'test_app/test.less\' %}')
        output = template.render(Context({}))
        self.assertEqual(output, '/static/test_app/test-186a766f4edc81bc2e686b81b15cd094.css')
        path_to_asset = os.path.join(
            settings.STATIC_ROOT,
            'test_app',
            'test-186a766f4edc81bc2e686b81b15cd094.css',
        )
        self.assertTrue(os.path.exists(path_to_asset))
        with open(path_to_asset, 'r') as asset_file:
            content = asset_file.read()
        expected = 'body {\n  color: blue;\n}\nbody .foo {\n  color: pink;\n}\n#foo .bar {\n  color: red;\n}\n'
        self.assertEqual(content, expected)

    def test_can_specify_multiple_transforms_on_the_template_tag(self):
        template = Template(
            '{% load frontend_tools %}{% frontend_tools less autoprefixer \'test_app/autoprefixer-test.less\' %}'
        )
        output = template.render(Context({}))
        self.assertEqual(output, '/static/test_app/autoprefixer-test-ef39ed210095e445a3f9e07d0129c01a.css')
        path_to_asset = os.path.join(
            settings.STATIC_ROOT,
            'test_app',
            'autoprefixer-test-ef39ed210095e445a3f9e07d0129c01a.css',
        )
        self.assertTrue(os.path.exists(path_to_asset))
        with open(path_to_asset, 'r') as asset_file:
            content = asset_file.read()
        expected = 'body {\n  color: blue;\n}\nbody .foo {\n  color: pink;\n}\n#foo {\n  border-radius: 100%;\n}\n'
        self.assertEqual(content, expected)

    def test_django_compressor_can_compress_css_with_the_css_filter(self):
        template = Template("""
        {% load compress frontend_tools %}
        {% compress css %}
            <style>
                body {
                    color: green;
                }
            </style>
            <link rel="stylesheet" href="{% frontend_tools less autoprefixer 'test_app/autoprefixer-test.less' %}">
        {% endcompress %}
        """)
        output = template.render(Context({}))
        output = output.strip()
        self.assertEqual(output, '<link rel="stylesheet" href="/static/CACHE/css/c43b56d0a5c8.css" type="text/css" />')
        with open(os.path.join(settings.STATIC_ROOT, 'CACHE', 'css', 'c43b56d0a5c8.css'), 'r') as css_file:
            content = css_file.read()
        expected = 'body{color:green}\nbody{color:#00f}body .foo{color:pink}#foo{border-radius:100%}'
        self.assertEqual(content, expected)

    def test_django_compressor_can_compress_js_with_the_js_filter(self):
        template = Template("""
        {% load compress static %}
        {% compress js %}
            <script>
                (function() { // Dead code that should be eliminated
                    var foo = 1;
                    var bar = 10;
                })();
                window.foo = 1; // This should be preserved
            </script>
            <script src={% static 'test_app/test.js' %}></script>">
        {% endcompress %}
        """)
        output = template.render(Context({}))
        output = output.strip()
        self.assertEqual(output, '<script type="text/javascript" src="/static/CACHE/js/e600b28a0955.js"></script>')
        with open(os.path.join(settings.STATIC_ROOT, 'CACHE', 'js', 'e600b28a0955.js'), 'r') as js_file:
            content = js_file.read()
        expected = 'window.foo=1;\nvar foo="bar",bar=function(){return foo};module.exports=bar;'
        self.assertEqual(content, expected)

    def test_compressed_css_automatically_prepends_to_relative_urls(self):
        template = Template("""
        {% load compress static %}
        {% compress css %}
            <link rel="stylesheet" href="{% static 'test_app/relative-url-test.css' %}">
        {% endcompress %}
        """)
        output = template.render(Context({}))
        output = output.strip()
        self.assertEqual(output, '<link rel="stylesheet" href="/static/CACHE/css/c2081c922dcf.css" type="text/css" />')
        with open(os.path.join(settings.STATIC_ROOT, 'CACHE', 'css', 'c2081c922dcf.css'), 'r') as js_file:
            content = js_file.read()
        expected = '#foo{background:url(/static/test_app/foo/bar.png)}#bar{background:url(/static/test_app/foo/bar/woo.png)}#zoo{background:url(/static/foo/bar.png)}#woo{background:url(/static/test_app/../foo/bar.png)}'
        self.assertEqual(content, expected)

        template = Template("""
        {% load compress static %}
        {% compress css %}
            <link rel="stylesheet" href="{% static 'test_app/css/relative-url-test.css' %}">
        {% endcompress %}
        """)
        output = template.render(Context({}))
        output = output.strip()
        self.assertEqual(output, '<link rel="stylesheet" href="/static/CACHE/css/6659bb83ddcd.css" type="text/css" />')
        with open(os.path.join(settings.STATIC_ROOT, 'CACHE', 'css', '6659bb83ddcd.css'), 'r') as js_file:
            content = js_file.read()
        expected = '#foo{background:url(/static/test_app/css/foo/bar.png)}#bar{background:url(/static/test_app/css/foo/bar/woo.png)}#zoo{background:url(/static/foo/bar.png)}#woo{background:url(/static/test_app/css/../foo/bar.png)}'
        self.assertEqual(content, expected)

    def test_can_pipe_bootstrap_from_less_to_autoprefixer_to_compress_css(self):
        """
        This ensures that the services can handle a real-world use case.
        Less is mixed in just to stress-test things.
        """
        output = compress_css(autoprefixer(less(BOOTSTRAP_CSS_FILE)))
        with open(BOOTSTRAP_CSS_EXPECTED_OUTPUT_FILE, 'r') as css_file:
            expected = css_file.read()
        self.assertEqual(output, expected)