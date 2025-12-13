from django.conf import settings


def site_config(request):
    return {"config": settings.SITE_CONFIG}