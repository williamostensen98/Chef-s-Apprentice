from django.contrib import admin
from django.contrib.admin import site


# from .models import Profile

# Register your models here.
# admin.site.register(User)





site.disable_action('delete_selected')
def change_view(self, request, object_id=None, form_url='', extra_context=None):
    return super().change_view(request, object_id, form_url,
                               extra_context=dict(show_delete=False))
