from django.conf import settings

def rollbar_access_token(request):
    try:
        return {
            'ROLLBAR_ACCESS_TOKEN_JS': settings.ROLLBAR_ACCESS_TOKEN_JS,
            'ROLLBAR_ENVIRONMENT_JS': settings.ROLLBAR['environment'],
        }
    except AttributeError:
        return {}
