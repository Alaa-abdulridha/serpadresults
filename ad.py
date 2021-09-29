import requests
from serpapi import GoogleSearch
import json
import os
import urllib.parse as urlparse
from urllib.parse import urlencode

path = os.path.dirname(os.path.abspath(__file__))
ad_results = []
api_key = "YOUR API KEY"
query_search = "Coffee"
output_file = path+'/test.json'

engines = [
  {"name": "google", "query": "q", "ad_param": "ads"},
  # {"name": "baidu", "query": "q", "ad_param": ""},
  {"name": "bing", "query": "q", "ad_param": "ads"},
  {"name": "duckduckgo", "query": "q", "ad_param": "ads"},
  {"name": "yahoo", "query": "p", "ad_param": "ads_results"},
  # {"name": "yandex", "query": "text", "ad_param": ""},
  # {"name": "ebay", "query": "_nkw", "ad_param": ""},
  {"name": "youtube", "query": "search_query", "ad_param": "ads_results"},
  {"name": "walmart", "query": "query", "ad_param": "ads_results"},
  # {"name": "home_depot", "query": "q", "ad_param": ""},
]

def get_next(engine, results):
  out = []
  current = []

  if engine["ad_param"] in results:
    ads = results[engine['ad_param']]
    out = out + ads
  
  current.append(results.get('serpapi_pagination').get('current'))

  while 'next' in results.get('serpapi_pagination'):
    url = results.get('serpapi_pagination').get('next')

    url_parse = urlparse.urlparse(url)
    query = url_parse.query
    url_dict = dict(urlparse.parse_qsl(query))
    url_dict.update(params)
    url_new_query = urlparse.urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    new_url = urlparse.urlunparse(url_parse)

    response = requests.get(new_url, timeout=60000)

    results = dict(json.loads(response.text))

    if "error" in results:
      print("oops error: ", results["error"])
      break

    if results.get('serpapi_pagination').get('current') in current:
      break

    current.append(results.get('serpapi_pagination').get('current'))

    if engine["ad_param"] in results:
      ads = results[engine['ad_param']]
      out = out + ads

for engine in engines:
  params = {
    "engine": engine["name"],
    engine["query"]: query_search,
    "api_key": api_key
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  if "error" in results:
    print("oops error: ", results["error"])
    continue
  
  next_results = get_next(engine, results)
  if next_results:
    ad_results.append({"name": engine["name"], "value": next_results})

with open(output_file, 'w') as fout:
  json.dump(ad_results , fout)
