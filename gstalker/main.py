import json
from time import sleep

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

    def parse_event_page(self, res):
        commits = []
        if res is not None:
            res_json = res.json()
            pushes = [_ for _ in res_json if _['type'] == 'PushEvent']
            for commit in pushes[0]['payload']['commits']:
                commits.append({'repo': pushes[0]['repo']['url'], 'sha': commit['sha']})
        return commits

    def validate_commit(self, payload):
        files_changed = [_['filename'].lower() for _ in payload['files']]
        for item in files_changed:
            if item in ['requirements.txt', 'package.json']:
                print('Found an item: {}'.format(item))

    def get_new_commits_by_file(self):
        for i in range(0, 10):
            events = self.get_events(page=i)
            if events is not None:
                commits = self.parse_event_page(events)
                for commit in commits:
                    commit_metadata = self.get_commit(commit['repo'], commit['sha'])
                    self.validate_commit(commit_metadata)
                    sleep(0.5)


def main():
    grabber = GStalker()
    grabber.get_new_commits_by_file()


if __name__ == '__main__':
    main()
