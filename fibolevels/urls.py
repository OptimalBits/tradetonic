from django.conf.urls.defaults import *

urlpatterns = patterns( 'tradetonic.fibolevels.views',
                        url(r'^quote/(?P<quote_id>[A-Z]+[0-9]+)$', 'update_chart'),
                        url(r'^params/(?P<quote_id>[A-Z]+[0-9]+)$', 'update_params'),
                        url(r'^', 'levels') )
                        

