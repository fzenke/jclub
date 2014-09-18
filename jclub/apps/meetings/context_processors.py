from django.conf import settings

def branding(request):
    return {'BRANDING': settings.BRANDING}