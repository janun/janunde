from django.conf import settings


def google_verification_id(request):
    try:
        return {
            "GOOGLE_VERIFICATION_ID": settings.GOOGLE_VERIFICATION_ID,
        }
    except AttributeError:
        return {}
