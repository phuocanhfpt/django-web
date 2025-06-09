from .models import SiteSetting

def site_settings(request):
    try:
        settings = SiteSetting.objects.first()
    except Exception:
        settings = None
    return {'site_settings': settings} 