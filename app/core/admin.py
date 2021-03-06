from django.conf import settings
from django.contrib import admin as default_admin


class AdminSite(default_admin.AdminSite):
    site_header = settings.SITE_HEADER
    index_title = settings.INDEX_TITLE


admin = AdminSite(name='site')
