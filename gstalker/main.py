import json

import requests


class GStalker(object):

    def __init__(self):
        self.load_config('../config/config.json')
        self.etag = None
        self.event_url = 'https://api.github.com/events'

    def load_config(self, tgt_file):
        """Load the github auth data."""
        with open(tgt_file, 'r') as infile:
            self.config = json.load(infile)

    def get_events(self, page=None):
        """Get the events stream from this URL, there are many pages but in general it seems we only get a few
        we cannot handle the entire GitHub stream."""

        if page is None:
            page = 1
        if self.etag is not None:
            headers = {'Etag': '\'{}\''.format(self.etag)}
        else:
            headers = {}
        url = '{}?page={}'.format(self.event_url, page)
        obj = requests.get(url, headers=headers, auth=(self.config['user'], self.config['pass']))
        if obj.status_code == 200:
            print('returning obj')
            if 'Etag' in obj.headers:
                self.etag = obj.headers['Etag']
            return obj
        else:
            print(obj.status_code)
            return None

    def get_commit(self, repo, sha):
        url = '{}/commits/{}'.format(repo, sha)
        print(url)
        vals = requests.get(url)
        if vals.status_code == 200:
            payload = vals.json()
            return payload
            # print(files_changed)
        else:
            print('bad status code: {}'.format(vals.status_code))


def main():
    etag = None

    grabber = GStalker()

    event_url = 'https://api.github.com/events'
    for i in range(0, 5):
        objs = grabber.get_events(event_url, etag)
        etag = objs.headers['Etag']
        if objs is not None:
            thing = objs.json()
            print('Got: {}'.format(len(thing)))
            pushes = [_ for _ in thing if _['type'] == 'PushEvent']
            for commit in pushes[0]['payload']['commits']:
                repo = pushes[0]['repo']['url']
                sha = commit['sha']
                grabber.get_commit(repo, sha)


if __name__ == '__main__':
    main()
