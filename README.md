# django-frontend-tools

- Less
- Autoprefixer
- CleanCSS
- UglifyJS

Integrates with django-compressor for css/js compression.

Runs a node process in the background for some nice performance improvements.

This is an in-progress rewrite of some old gulp-based frontend tooling. It's reasonably well tested, but was built for a particular project's workflow, so it still needs a lot of love to make it more broadly useful.

The primary benefit of frontend-tools is that it offers a bunch of performance improvements over binaries/gulp/grunt/etc. If DEBUG is False, it caches everything, in dev it'll rely on file caching so that the less output is up to date.

Requires a fairly recent version of django-node's master branch...
```
pip install -e git+https://github.com/markfinger/django-node.git@a360a6f497af33761ebfb012dc51877769e72789#egg=django-node
pip install -e git+https://github.com/markfinger/django-frontend-tools.git@#egg=django-frontend-tools
```

```python
# in settings

INSTALLED_APPS = (
    # ...
    'django_compressor',
    'django_node',
    'django_frontend_tools',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_frontend_tools',
    ),
}

COMPRESS_CSS_FILTERS = [
    'django_frontend_tools.filters.CompressCSSFilter',
]

COMPRESS_JS_FILTERS = [
    'django_frontend_tools.filters.CompressJSFilter',
]

STATICFILES_FINDERS = (
    # ...
    'compressor.finders.CompressorFinder',
)
```

```html
{% load frontend_tools compress %}

{% compress css %}
  <link rel="stylesheet" href="{% frontend_tools less autoprefixer 'path/to/file.less' %}">
{% endcompress %}

{% compress js %}
  <script>
    // ...
  </script>
{% endcompress %}
```
