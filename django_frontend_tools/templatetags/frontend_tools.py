import os
from urlparse import urljoin
from django import template
from django.contrib.staticfiles import finders
from django.conf import settings
from ..transforms import autoprefixer, less
from ..utils import version_file_name
from ..exceptions import MissingTemplateTagArgument, CannotFindFile

register = template.Library()

TRANSFORMS = {
    'autoprefixer': autoprefixer,
    'less': less,
}

@register.tag('frontend_tools')
def frontend_tools_tag(parser, token):
    """
    Example usage
    ```
        {% load frontend_tools %}

        <link rel="stylesheet" href="{% frontend_tools less autoprefixer 'path/to/file.less' %}">
    ```
    """
    options = token.contents.split()

    transforms = options[1:-1]
    asset = options[-1]

    if not transforms or not asset:
        raise MissingTemplateTagArgument(options)

    # Remove quotation marks from the asset name
    asset = asset.strip('\'').strip('\"')

    return FrontendToolsNode(transforms, asset)


TRANSFORMED_ASSETS_CACHE = {}


class FrontendToolsNode(template.Node):
    transforms = ()
    asset = None
    path_to_asset = None
    versioned_file = None
    path_to_versioned_file = None

    def __init__(self, transforms, asset):
        self.transforms = tuple([TRANSFORMS[transform] for transform in transforms])
        self.asset = asset
        self.path_to_asset = finders.find(self.asset)
        if not self.path_to_asset:
            raise CannotFindFile(self.asset)

    def write_to_file(self, transformed):
        if not os.path.isdir(os.path.dirname(transformed['output_path'])):
            os.makedirs(os.path.dirname(transformed['output_path']))
        with open(transformed['output_path'], 'w') as versioned_file:
            versioned_file.write(transformed['content'])

    def get_cache_key(self):
        return self.transforms + (self.path_to_asset,)

    def render(self, context):
        transformed = {
            'content': None,
            'relative_path': self.asset,
            'absolute_path': self.path_to_asset,
            'output_path': os.path.join(settings.STATIC_ROOT, self.asset),
        }

        for i, transform in enumerate(self.transforms):
            if i == 0:
                transformed['content'] = transform(path_to_file=transformed['absolute_path'])
            else:
                transformed['content'] = transform(transformed['content'])

            if hasattr(transform, 'file_name_transform'):
                for key in ('relative_path', 'absolute_path', 'output_path'):
                    transformed[key] = transform.file_name_transform(transformed[key], transformed['content'])

        for key in ('relative_path', 'absolute_path', 'output_path'):
            transformed[key] = version_file_name(transformed[key], transformed['content'])

        self.write_to_file(transformed)
        output = urljoin(settings.STATIC_URL, transformed['relative_path'])

        return output
