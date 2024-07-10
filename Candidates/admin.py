# project/admin.py

from django.contrib.admin import AdminSite
from django.urls import reverse
from django.http import HttpResponseRedirect

class CustomAdminSite(AdminSite):
    site_header = 'Custom Admin Dashboard'  # Customize the admin site header
    
    def index(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('admin_dashboard'))
        
custom_admin_site = CustomAdminSite(name='custom_admin')
