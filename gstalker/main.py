# -*- coding: utf-8 -*-

from time import sleep, time
from datetime import datetime as dt

import requests
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from gstalker.utils import load_config, parse_for_meta
from gstalker.models import RepositoryMoment
from gstalker.database import engine


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

    def __init__(self, config_path=None, init_db=True):
        if config_path is None:
            self.config_path = './config/config.json'
        else:
            self.config_path = config_path
        self.config = load_config(self.config_path)
        self.etag = None
        self.event_url = 'https://api.github.com/events'
        self.remaining_requests = 50
        self.request_hour_start = dt.now()
        self.auth = (self.config.get('github_api').get('user'), self.config.get('github_api').get('pass'))
        if init_db:
            print('Initializing DB')
            self.db = scoped_session(sessionmaker(bind=engine(self.config['db'])))

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
        """From the event page, extract recent pushes (so we can peek into their commits)"""
        commits = []
        if res is not None:
            res_json = res.json()
            pushes = [_ for _ in res_json if _['type'] == 'PushEvent']
            for commit in pushes[0]['payload']['commits']:
                commits.append({'repo': pushes[0]['repo']['url'], 'sha': commit['sha']})
        return commits

    def validate_commit(self, payload):
        """Check if a commit contains a file we are looking for."""
        ret_vals = []
        assert type(payload) is dict
        check_values = ['requirements.txt', 'package.json']
        for item in payload['files']:
            for check in check_values:
                if item.get('filename').lower().endswith(check):
                    url_info = parse_for_meta(item.get('raw_url'))
                    repo_data = {
                        'repo_name': url_info['repo'],
                        'sha': payload.get('sha'),
                        'user': url_info['user'],
                        'repo_type': check,
                        'check_state': 'FOUND',
                        'target_file_url': item.get('raw_url')
                    }
                    ret_vals.append(repo_data)
        return ret_vals

    def store_commit(self, item):
        """Store the commit in the database."""
        c = RepositoryMoment(**item)
        self.session.add(c)
        try:
            self.session.commit()
        except IntegrityError as err:
            print(err)
            self.session.rollback()
        except SQLAlchemyError as err:
            print(err)
            self.session.rollback()

    def get_new_commits_by_file(self):
        for i in range(0, 10):
            events = self.get_events(page=i)
            if events is not None:
                commits = self.parse_event_page(events)
                for commit in commits:
                    commit_metadata = self.get_commit(commit['repo'], commit['sha'])
                    results = self.validate_commit(commit_metadata)
                    for item in results:
                        self.store_commit(item)
                    sleep(0.5)


def main():
    grabber = GStalker()
    grabber.get_new_commits_by_file()


if __name__ == '__main__':
    main()
