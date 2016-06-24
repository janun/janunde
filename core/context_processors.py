from django.conf import settings

def rollbar_access_token(request):
    try:
        return {'ROLLBAR_ACCESS_TOKEN': settings.ROLLBAR_ACCESS_TOKEN}
    except AttributeError:
        return {}
