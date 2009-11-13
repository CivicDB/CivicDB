import mimetypes
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group

class Provider(models.Model):
    """
        
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User) 
    created = models.DateField()
    #perhaps we should have a separate user login for each 
    #provider contact, but for now we'll just do it like this
    
    def __unicode__(self): return '%s' % self.name
    
class ProviderContact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    primary = models.BooleanField(default=False)
    provider = models.ForeignKey(Provider)
    def __unicode__(self): return '%s' % self.name
    

frequency_choices = (
        ('hourly' , 'hourly'),
        ('daily' , 'daily'),
        ('weekly' , 'weekly'),
        ('biweekly' , 'biweekly'),
        ('monthly' , 'monthly'),
        ('quarterly' , 'quarterly'),
        ('annually' , 'annually'))
        
mime_choices = ((k,v) for k,v in mimetypes.types_map.items())

class DataSeries(models.Model):
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider)
    file_format = models.CharField(max_length=255, choices=mime_choices)
    data_frequence = models.CharField(max_length=255, choices=frequency_choices)
    data_division = models.TextField(
        help_text="way other than time that the files are divided up")
    comment = models.TextField()
    naming_convention = models.CharField(max_length=255, 
        help_text = "template of how files in the series are named.  defaults to 'starts with'")
    def __unicode__(self): return '%s' % self.name
    
class DataMapping(models.Model):
    """
    files which describe or encode mapping the data series
    """
    name = models.CharField(max_length=255)
    mapping = models.FileField(upload_to=settings.DATA_UPLOAD_PATH)
    series = models.ForeignKey(DataSeries)
    def __unicode__(self): return '%s' % self.name
    
status = (
        ('unprocessed' , 'unprocessed'),
        ('in-process' , 'in-process'),
        ('failed' , 'failed'),
        ('processed' , 'processed'))

        
class DataFile(models.Model):
    series = models.ForeignKey(DataSeries)
    data = models.FileField(upload_to = '.')
    status = models.CharField(max_length=255, blank=True, null=True, default='unprocessed')
    processor = models.CharField(max_length=255)
    starts_on = models.DateTimeField(auto_now = True)
    end_on = models.DateTimeField(auto_now = True)
    loaded_on = models.DateTimeField(auto_now = True)
    size = models.FloatField(blank=True, null=True)
    def __unicode__(self): return '%s' % self.series


