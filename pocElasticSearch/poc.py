# make sure ES is up and running
#import requests
#res = requests.get('http://localhost:9200')
#print(res.content)

#connect to our cluster
from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.transport.connection_pool.connection.headers.update({'Content-Type': 'application/json'})

##sms = {
##    "id": "1",
##    "date": "15 sept. 2011 09:05:28",
##    "num_tel": 477,
##    "incomnig": 0,
##    "content": "On peut se rejoindre quelque part? Tu as cours ou ?"
##}
##
##res = es.index(index = "messages", doc_type = "message",
##               id = 1, body = sms)
##print(res)

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res['created'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
