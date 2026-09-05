from django.conf import settings
from .models import SiteSetting

def business_context(request):
    try:
        site_setting = SiteSetting.load()
    except Exception:
        site_setting = None

    return {
        'site_setting': site_setting,
        'business_info': getattr(settings, 'BUSINESS_INFO', {}),
    }
