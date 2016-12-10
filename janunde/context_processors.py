from django.conf import settings

def rollbar_access_token(request):
    try:
        return {
            'ROLLBAR_ACCESS_TOKEN_JS': settings.ROLLBAR_ACCESS_TOKEN_JS,
            'ROLLBAR_ENVIRONMENT_JS': settings.ROLLBAR['environment'],
        }
    except AttributeError:
        return {}


def freesurveycreator_id(request):
    try:
        return {
            'FREESURVEYCREATOR_ID': settings.FREESURVEYCREATOR_ID,
        }
    except AttributeError:
        return {}


def betabanner(request):
    try:
        return {
            'BETABANNER': settings.BETABANNER,
        }
    except AttributeError:
        return {}

def mouseflow_id(request):
    try:
        return {
            'MOUSEFLOW_ID': settings.MOUSEFLOW_ID,
        }
    except AttributeError:
        return {}

def piwik_url(request):
    try:
        return {
            'PIWIK_URL': settings.PIWIK_URL,
        }
    except AttributeError:
        return {}

def google_verification_id(request):
    try:
        return {
            'GOOGLE_VERIFICATION_ID': settings.GOOGLE_VERIFICATION_ID,
        }
    except AttributeError:
        return {}
