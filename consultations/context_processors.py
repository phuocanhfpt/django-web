from .models import FooterSettings, FooterMenuGroup

def footer_settings(request):
    footer = FooterSettings.objects.first()
    menu_groups = FooterMenuGroup.objects.filter(is_active=True).prefetch_related('menus')
    return {
        'footer': footer,
        'menu_groups': menu_groups
    } 