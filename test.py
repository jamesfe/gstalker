import json

import requests


with open('./config.json', 'r') as infile:
    gh = json.load(infile)

event_url = 'https://api.github.com/events'


def get_events(url, etag=None):
    if etag:
        headers = {'Etag': '\'{}\''.format(etag)}
    else:
        headers = {}
    obj = requests.get(event_url, headers=headers, auth=(gh['user'], gh['pass']))
    if obj.status_code == 200:
        print('returning obj')
        return obj
    else:
        print(obj.status_code)
        return None


def get_commit(repo, sha):
    url = '{}/commits/{}'.format(repo, sha)
    print(url)
    vals = requests.get(url)
    if vals.status_code == 200:
        payload = vals.json()
        files_changed = [_['filename'] for _ in payload['files']]
        print(files_changed)
    else:
        print('bad status code: {}'.format(vals.status_code))


etag = None

for i in range(0, 5):
    objs = get_events(event_url, etag)
    print(objs.headers)
    etag = objs.headers['Etag']
    print('ETAG: ', etag)
    if objs is not None:
        thing = objs.json()
        print('Got: {}'.format(len(thing)))
        pushes = [_ for _ in thing if _['type'] == 'PushEvent']
        for commit in pushes[0]['payload']['commits']:
            repo = pushes[0]['repo']['url']
            sha = commit['sha']
            get_commit(repo, sha)
