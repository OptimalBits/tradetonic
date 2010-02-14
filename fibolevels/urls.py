from django.conf.urls.defaults import *

urlpatterns = patterns( 'tradetonic.fibolevels.views',
                        url(r'^quote/(?P<quote_id>[A-Z]+[0-9]+)/(?P<resolution>[0-9]+)$', 'update_chart'),
                        url(r'^levels/(?P<quote_id>[A-Z]+[0-9]+)/(?P<resolution>[0-9]+)$', 'update_levels'),
                        url(r'^params/(?P<quote_id>[A-Z]+[0-9]+)/(?P<resolution>[0-9]+)$', 'update_params'),
                        url(r'^menus/quotes/(?P<quote_type>[A-Z]+)$', 'populate_quotes'),
                        url(r'^charts/', 'show_charts'),
                        url(r'^bargains/', 'show_bargains'),
#                        url(r'','show_charts'),
                      )
                        

