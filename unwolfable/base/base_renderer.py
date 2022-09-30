import json
from rest_framework.renderers import JSONRenderer


class BaseJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def check_errors(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        if errors is not None:
            return super(BaseJSONRenderer, self).render(data)

    def render(self, data, media_type=None, renderer_context=None):
        if not data:
            return None
        return self.check_errors(data) or json.dumps({'data': data})
