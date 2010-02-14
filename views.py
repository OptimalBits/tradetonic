from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, NoReverseMatch

from tradetonic.tabmenu.models import *

def home ( request, tabs ): 
    select_tab( tabs, "Home")
    return render_to_response('tradetonic.html', {'tabs': tabs})
    