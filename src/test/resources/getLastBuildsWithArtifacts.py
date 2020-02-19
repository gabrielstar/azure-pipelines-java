import requests

url = r"https://dev.azure.com/gstarczewski/jmeter/_apis/build/builds"
payload = {'api-version': '5.1', 'resultFilter': 'succeeded'}
r = requests.get(url, payload)
artifact = "JMeterReport"
count = r.json()['count']
values = r.json()['value']
previous_builds_number = 2
# fetch last successful builds ids
ids = list(map(lambda v: v['id'], values))[:previous_builds_number]

payload = {'api-version': '5.1', 'artifactName': artifact}
for id in ids:
    r = requests.get("%s/%s/artifacts" % (url, id))
    try:
        download_url = r.json()['value'][0]['resource']['downloadUrl']
        r = requests.get(download_url)
        with open("tmp/%s_%s.zip" % (id, artifact), "wb") as f:
            f.write(r.content)
    except IOError:
        print "Could not fetch the file for the build %s" % id
    except:
        print "Could not get artifact for the build %s" % id
