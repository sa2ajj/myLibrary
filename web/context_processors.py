"""
...
"""

from django.conf import settings

def site(request):
    """..."""

    data = {
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_SUBTITLE': settings.SITE_SUBTITLE,
        'MAIN_MENU': settings.MAIN_MENU,
        'COMPANY': settings.COMPANY
    }

    if request.user.is_authenticated():
        data['USER_OBJECT'] = request.user

        if user.is_staff:
            data['USER_ADMIN'] = 'Admin'

        data['USER_NAME'] = request.user.username
        # TODO: change to some configurable thingie
        data['USER_ACTION_URL'] = settings.LOGOUT_URL
    else:
        data['USER_ACTION_URL'] = settings.LOGIN_URL

    return data
