from django.conf.urls.defaults import *
from django.views.generic import list_detail
from views import *
from models import *



urlpatterns = patterns('',
    (r'^$', static, {'template':'index.html'}),
    (r'^contact/$', static, {'template':'contact.html'}),

    (r'^datafiles/$', list_view, {'model' : DataFile}),
    (r'^datafiles/create/$', upload_file),
    (r'^datafiles/(?P<id>\d+)/$', detail_view, {'model' : DataFile}),
    (r'^datafiles/(?P<id>\d+)/edit/$', datafile_edit),
    
    
    (r'^dataseries/$', list_view, {'model' : DataSeries}),
    (r'^dataseries/create/$', dataseries_create),
    (r'^dataseries/(?P<id>\d+)/edit/$', dataseries_create),
    (r'^dataseries/(?P<id>\d+)/$', detail_view, {'model' : DataSeries}),
)
    
