import os
import random
import posixpath
from django.conf import settings
from django.template import Library, Node
from django.db.models import get_model
     
register = Library()
     
def is_image_file(filename):
    """Does `filename` appear to be an image file?"""
    img_types = [".jpg", ".jpeg", ".png", ".gif"]
    ext = os.path.splitext(filename)[1]
    return ext in img_types

@register.simple_tag
def random_image(path):
    """
    Select a random image file from the provided directory
    and return its href. `path` should be relative to MEDIA_ROOT.
    
    Usage:  <img src='{% random_image "images/whatever/" %}'>
    """
    fullpath = os.path.join(settings.MEDIA_ROOT, path)
    filenames = [f for f in os.listdir(fullpath) if is_image_file(f)]
    pick = random.choice(filenames)
    return posixpath.join(settings.MEDIA_URL, path, pick)
     
     
     
class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all().order_by('-date_created')[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    res = LatestContentNode(bits[1], bits[2], bits[4])
    return res

get_latest = register.tag(get_latest)



@register.filter
def truncatewords_by_chars(value, arg):
  """
  Truncate words based on the number of characters
  based on original truncatewords filter code
  
  Receives a parameter separated by spaces where each field means:
   - limit: number of characters after which the string is truncated
   - lower bound: if char number is higher than limit, truncate by lower bound
   - higher bound: if char number is less than limit, truncate by higher bound
  """
  from django.utils.text import truncate_words
  try:
    args = arg.split(' ')
    limit = int(args[0])
    lower = int(args[1])
    higher = int(args[2])
  except ValueError: # Invalid literal for int().
    return value
  if len(value) >= limit:
    return truncate_words(value, lower)
  if len(value) < limit:
    return truncate_words(value, higher)
