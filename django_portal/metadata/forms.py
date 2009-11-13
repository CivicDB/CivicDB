from django import forms
from models import *

class DataFileAddForm(forms.ModelForm):
    class Meta:
        model = DataFile


class DataSeriesAddForm(forms.ModelForm):
    class Meta:
        model = DataSeries
        