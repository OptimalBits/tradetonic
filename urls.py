from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns( '',
    (r'^tradetonic', include ('tradetonic.fibolevels.urls')),

    # Static Media
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/Users/manuel/Django-projects/tradetonic/media'})
    
)
