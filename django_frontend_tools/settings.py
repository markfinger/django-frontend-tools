from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_FRONTEND_TOOLS', {})

CACHE = setting_overrides.get(
    'CACHE',
    not settings.DEBUG
)

CACHE_AUTOPREFIXER = setting_overrides.get(
    'CACHE_AUTOPREFIXER',
    CACHE,
)

CACHE_LESS = setting_overrides.get(
    'CACHE_LESS',
    CACHE,
)

CACHE_COMPRESSED_CSS = setting_overrides.get(
    'CACHE_COMPRESSED_CSS',
    CACHE,
)

CACHE_COMPRESSED_JS = setting_overrides.get(
    'CACHE_COMPRESSED_JS',
    CACHE,
)