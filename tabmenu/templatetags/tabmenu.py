from django import template
#from blog.models import BlogEntry, Tag
from django.http import Http404

register = template.Library()
        
# A blog bar
@register.inclusion_tag('tabmenu.html')
def tabmenu( tabs ):
    return {'tabs': tabs}
   
