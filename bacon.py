from urllib.request import urlopen,Request
from urllib.parse import urlencode
import json
import sys

endpoint = "http://data.linkedmdb.org/sparql?"
print("Gimme a name:")
kevin = input()

getActorsByName = """
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?actor ?aname WHERE {
?actor a movie:actor .
?actor movie:actor_name ?aname.
FILTER (regex(?aname,"^""" + kevin + """","i"))
}
"""

params = { 'query': getActorsByName }
paramstr = urlencode(params)

req = Request(endpoint+paramstr)
req.add_header('Accept','application/sparql-results+json')
page = urlopen(req)
text = page.read().decode('utf-8')
page.close()

toJson = json.loads(text)

actorsDict = {}

# iterate over results
for binding in toJson['results']['bindings']:
        actorsDict[binding['aname']['value']] = binding['actor']['value']

if not actorsDict:
	print("No actors found")
	sys.exit(0)

print("Here's a list of actors you can choose from: ")
for key in actorsDict:
        print(key)

print("Choose an actor: ")
specificActor = input()

if (specificActor in actorsDict):
	selectedURI = actorsDict[specificActor]
else:
	print("No such actor")
	sys.exit(0)

getCoActors = """
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX lmdba: <http://data.linkedmdb.org/resource/actor/>
PREFIX lmdbf: <http://data.linkedmdb.org/resource/film/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT(?filmName) ?actorName WHERE {
	?film movie:actor <""" + selectedURI+"""> .
	?film movie:actor ?oneDeg .
	?film rdfs:label ?filmName .
	?oneDeg movie:actor_name ?actorName .
	FILTER(?oneDeg != <""" + selectedURI+""">)
}

"""

params = { 'query': getCoActors }
paramstr = urlencode(params)

req = Request(endpoint+paramstr)
req.add_header('Accept','application/sparql-results+json')
page = urlopen(req)
text = page.read().decode('utf-8')
page.close()

toJsonCoActors = json.loads(text)

print("Here's a list of actors and the films they starred along with " + specificActor + " in: ")
for binding in toJsonCoActors['results']['bindings']:
       print(binding['actorName']['value'],"in", binding['.0']['value'])

