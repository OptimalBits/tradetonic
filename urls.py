from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from tradetonic.tabmenu.models import *


tabs = ( Tab("Home", "", 'tradetonic.views.home'),
         Tab("Fibonacci Levels", "fibonacci", include('tradetonic.fibolevels.urls'),
            ( Tab("Chart","charts", ""), Tab("Money Management","money", ""), Tab("Bargains","bargains", "") ) ), 
         Tab("Tutorials", "tutorials", "tradetonic.views.tutorials"), 
         Tab("News & Press", "news", "tradetonic.views.news"),
         Tab("Disclaimer", "news", "tradetonic.views.news"),
         Tab("Contact Us", "contact", "tradetonic.views.contact") )


urlpatterns = patterns('',
    # Static Media
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/Users/manuel/dev/Django-projects/tradetonic/media'})
)

for t in tabs:
	urlpatterns += patterns('', t.url_pattern(tabs) )
	print t.url_pattern(tabs)
    
    
    



