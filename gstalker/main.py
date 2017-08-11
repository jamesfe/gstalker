import json
from time import sleep, time
from datetime import datetime as dt

import requests


class GStalker(object):

    def make_request(self, url, headers=None, auth=None):
        """Make a request but also keep our rates down."""
        # TODO: Add a specific sleep based on requests remaining.
        if headers is None:
            headers = {}
        if self.remaining_requests > 0:
            res = requests.get(url, headers=headers, auth=auth)
            self.remining_requests = res.headers['X-RateLimit-Remaining']
            self.reset_time = res.headers['X-RateLimit-Reset']
            return res
        elif self.remaining_requests <= 0:
            res = requests.get(url, headers=headers, auth=auth)
            if 'X-RateLimit-Reset' not in res.headers:
                print('Not receiving rate limit reset in headers, returning None.')
                return None
        elif self.reset_time is not None:
            seconds_to_wait = self.reset_time - time()
            print('Sleeping for {} seconds, rate limits too low.'.format(seconds_to_wait))
            sleep(seconds_to_wait)
            res = self.make_request(url, headers, auth)
        else:
            print('No requests left.')
            return None

    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = './config/config.json'
        else:
            self.config_path = config_path
        self.load_config(self.config_path)
        self.etag = None
        self.event_url = 'https://api.github.com/events'
        self.remaining_requests = 50
        self.request_hour_start = dt.now()
        self.auth = (self.config['user'], self.config['pass'])

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
        obj = self.make_request(url, headers=headers, auth=self.auth)
        if obj.status_code == 200:
            if 'Etag' in obj.headers:
                self.etag = obj.headers['Etag']
            return obj
        else:
            print(obj.status_code)
            return None

    def get_commit(self, repo, sha):
        url = '{}/commits/{}'.format(repo, sha)
        print('Checking Commit: ', url)
        vals = self.make_request(url)
        if vals.status_code == 200:
            payload = vals.json()
            return payload
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
