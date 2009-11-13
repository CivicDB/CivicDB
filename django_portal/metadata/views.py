from datetime import datetime
import json
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.gis.feeds import Feed
from django.views.decorators.cache import cache_page
from django.template.defaultfilters import slugify
from models import *
from forms import *
from django.db.models import Count


def render_to_json(modelname, qs):
    interesting = {
        'datafile' : ['id','status','size'],
        'dataseries' : ['name','provider','file_format']
        }
    j = {modelname:[]}
    for item in qs:
        d = {}
        for k in interesting[modelname]:
            d[k] = getattr(item,k)
            if modelname == 'datafile':
                d['series_name'] = item.series.name
                d['series_id'] = item.series.id
        j[modelname].append(d)
    return HttpResponse(json.dumps(j), mimetype = "text/html")
    


def static(request, template):
    return render_to_response(template)
    return render_to_response('index.html',RequestContext(request,{
        'GKEY' : GOOGLE_API_KEY }))


def upload_file(request):
    if request.method == 'POST':
        form = DataFileAddForm(request.POST, request.FILES)
        print 'mp', form.is_multipart()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
    else:
        form = DataFileAddForm()
    return render_to_response('upload.html', {'form': form})


def datafile_edit(request, id):
    if request.method == 'POST':
        if id:
            op = DataFile.objects.get(pk=id)
            form = DataFileAddForm(request.POST, instance=op)
        else:
            form = DataFileAddForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        if id:
            op = DataFile.objects.get(pk=id)
            form = DataFileAddForm(instance=op)
        else:
            form = DataFileAddForm()
    return render_to_response("dataseries_create.html", RequestContext(request,{
        "form": form,
    }))    

    
def dataseries_create(request, dataseries_id=''):
    if request.method == 'POST':
        if dataseries_id:
            op = DataSeries.objects.get(pk=dataseries_id)
            form = DataSeriesAddForm(request.POST, instance=op)
        else:
            form = DataSeriesAddForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.date_created = datetime.now()
            p.dataseriesr = request.user
            p.save()
            form.save_m2m()
    else:
        if dataseries_id: 
            dataseries = dataseries.objects.get(id=dataseries_id)
            #pass this to template so it gets highlighted
        form = DataSeriesAddForm()
    return render_to_response("dataseries_create.html", RequestContext(request,{
        "form": form,
    }))
    
def list_view(request, model, id=''):
    modelname = model._meta.module_name
    ds = model.objects.all()
    format = request.GET.get('format','')
    if format == 'json':
        return render_to_json(modelname, ds)
    return render_to_response('%s_list.html' % modelname, RequestContext(request,{
        'object_list' : ds}))
        
def detail_view(request, model, id=''):
    modelname = model._meta.module_name
    ds = model.objects.get(pk=id)
    return render_to_response('%s_detail.html' % modelname, RequestContext(request,{
        'obj' : ds}))
        
def edit_view(request, model, id=''):
    ds = model.objects.get(pk=id)
    
