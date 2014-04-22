import flickrapi
import simplejson as json
import re
from HTMLParser import HTMLParser
import sys
from parser import Parser
import nltk
import codecs
from collections import defaultdict

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
dum_arr =['tiger','window']

all_objs = per_arr + air_arr + bike_arr + sofa_arr + tv_arr + other_arr +dum_arr

attr = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'red', 'violet', 'white', 'yellow', 'spotted', 'striped','long', 'round', 'rectangular', 'square', 'furry', 'smooth', 'rough', 'shiny', 'metallic', 'vegetation', 'wooden', 'wet']




def _fetcher(search_text):
  flickr = flickrapi.FlickrAPI(api_key, format='json')
  ret_dict = defaultdict(dict)
  for x in xrange(1,3):
    sets = flickr.photos_search(text=search_text,per_page='500', page=x,extras='description')
    sets = sets.replace('jsonFlickrApi', '').strip('()')
    jsets = json.loads( sets, object_hook=_decode_dict )
    photoset_group = jsets['photos']['photo']
    for photo in photoset_group:
      if strip_tags(photo['description']['_content'])!= '' and search_text in photo['description']['_content']:
        content = strip_tags(photo['description']['_content'])
        import unicodedata
        for sentence in sent.tokenize(unicodedata.normalize('NFKD', content).encode('ascii','ignore').strip().decode('utf8')):
          if len(sentence) < 150 and len(sentence) > 6:
            try :
              dep = sp.parseToStanfordDependencies(sentence)
              tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dep.dependencies]
              for tup in tupleResult:
                if (tup[0]=='amod') and (tup[1] in all_objs) and (tup[2] in attr):
                  print tup[1]
                  if tup[2] in ret_dict:
                    cnt = ret_dict[tup[2]]
                    cnt = cnt + 1
                    ret_dict[tup[2]] = cnt
                  else:
                    ret_dict[tup[2]] = 1
            except :
              pass
  return ret_dict



resp_writer = defaultdict(list)
for item in per_arr:
  resp_writer['person'].append(_fetcher(item))

with open("/Users/vgurswamy/Desktop/data.html","wb") as outfile:
  json.dump(resp_writer, outfile, indent = 4)

#for item in tv_arr:
#  resp_writer['tv'].append(_fetcher(item))

#for item in other_arr:
#  resp_writer[item].append(_fetcher(item))






