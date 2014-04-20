import flickrapi
import simplejson as json
import re
from HTMLParser import HTMLParser
import sys
from parser import Parser
import nltk
import codecs


api_key = '61145ac716dc622244c5f879a0bd0e5f'
sp = Parser()
sent = nltk.data.load('tokenizers/punkt/english.pickle')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    html = html.decode('latin-1')
    s.feed(html)
    return s.get_data()

def _decode_list(data):
  rv = []
  for item in data:
      if isinstance(item, unicode):
          item = item.encode('utf-8')
      elif isinstance(item, list):
          item = _decode_list(item)
      elif isinstance(item, dict):
          item = _decode_dict(item)
      rv.append(item)
  return rv

def _decode_dict(data):
  rv = {}
  for key, value in data.iteritems():
      if isinstance(key, unicode):
          key = key.encode('utf-8')
      if isinstance(value, unicode):
          value = value.encode('utf-8')
      elif isinstance(value, list):
          value = _decode_list(value)
      elif isinstance(value, dict):
          value = _decode_dict(value)
      rv[key] = value
  return rv

photoIds = []
per_arr = ['person', 'man', 'woman', 'girl', 'boy', 'kid']
air_arr = ['aeroplane', 'airplane']
bike_arr = ['bicycle', 'motorbike', 'bike']
sofa_arr = ['couch', 'sofa']
tv_arr =['tv','monitor']
other_arr = ['boat', 'bus', 'car', 'train', 'bottle', 'chair', 'dining table', 'potted plant',  'flower', 'laptop', 'tiger', 'window']
attr = {}
attr['color'] = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'red', 'violet', 'white', 'yellow']
attr['pattern'] = ['spotted', 'striped']
attr['shape'] = ['long', 'round', 'rectangular', 'square']
attr['texture'] = ['furry', 'smooth', 'rough', 'shiny', 'metallic', 'vegetation', 'wooden', 'wet']


def _fetcher(search_text):
  flickr = flickrapi.FlickrAPI(api_key, format='json')
  ret_list = []
  for x in xrange(1,2):
    sets = flickr.photos_search(text=search_text,per_page='500', page=x,extras='description')
    sets = sets.replace('jsonFlickrApi', '').strip('()')
    jsets = json.loads( sets, object_hook=_decode_dict )
    photoset_group = jsets['photos']['photo']
    for photo in photoset_group:
      if strip_tags(photo['description']['_content'])!= '':
        content = strip_tags(photo['description']['_content'])
        import unicodedata
        for sentence in sent.tokenize(unicodedata.normalize('NFKD', content).encode('ascii','ignore').strip().decode('utf8')):
          if len(sentence) < 150 and len(sentence) > 6:
            try :
              dep = sp.parseToStanfordDependencies(sentence)
              tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dep.dependencies]
              for tup in tupleResult:
                if tup[0]=='amod':
                  ret_str = tup[2] + '--' + tup[1]
                  ret_list.append(ret_str)
            except :
              pass
  return ' '.join( st for st in ret_list) 

resp_writer = {}

value = ''
for item in per_arr:
  value = value + _fetcher(item) 
resp_writer['person'] = value

value = ''
for item in air_arr:
  value = value + _fetcher(item) 
resp_writer['aeroplane'] = value

value = ''
for item in bike_arr:
  value = value + _fetcher(item) 
resp_writer['bike'] = value

value = ''
for item in sofa_arr:
  value = value + _fetcher(item) 
resp_writer['sofa'] = value

value = ''
for item in tv_arr:
  value = value + _fetcher(item)
resp_writer['tv'] = value

for item in other_arr:
  resp_writer[item] = _fetcher(item)


with open('/Users/vgurswamy/Desktop/data.html', 'w') as outfile:
  json.dump(resp_writer, outfile, indent = 4)




