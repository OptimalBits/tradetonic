from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns( '',
    # Static Media
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/Users/manuel/Django-projects/tradetonic/media'}),
   (r'^', include ('tradetonic.fibolevels.urls')),
)
