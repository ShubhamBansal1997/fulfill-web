from rest_framework.renderers import JSONRenderer


class FulfillApiRenderer(JSONRenderer):
    media_type = 'application/vnd.fulfill+json'
