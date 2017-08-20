# -*- coding: utf-8 -*-

from time import sleep, time
from datetime import datetime as dt

import requests
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from gstalker.utils import load_config, parse_for_meta, parse_js_dep, is_root_package_json
from gstalker.models import RepositoryMoment, Dependency
from gstalker.database import engine


class GStalker(object):

    def make_request(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            return res
        if res.status_code == 404:
            pass
            # TODO: Update the database, this is gone!
        else:
            print('Bad status code on get request: {}'.format(res.status_code))
            return None

    def make_api_request(self, url, headers=None, auth=None):
        """Make a request but also keep our rates down."""
        if headers is None:
            headers = {}
        if self.remaining_requests > 0:
            pre = time()
            res = requests.get(url, headers=headers, auth=auth)
            req_time = time() - pre
            self.remaining_requests = int(res.headers['X-RateLimit-Remaining'])
            self.reset_time = int(res.headers['X-RateLimit-Reset'])
            # We calculate the time it takes to make a request, then we multiply that by the number left and see
            # how long we should wait.
            moment_to_wait = (req_time * self.remaining_requests) / (self.reset_time - time())
            print('Requesting {}, Left: {}, Waiting: {}'.format(url, self.remaining_requests, moment_to_wait))
            if moment_to_wait > 0:
                sleep(moment_to_wait)
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
            res = self.make_api_request(url, headers, auth)
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
        obj = self.make_api_request(url, headers=headers, auth=self.auth)
        if obj.status_code == 200:
            if 'Etag' in obj.headers:
                self.etag = obj.headers['Etag']
            return obj
        else:
            print(obj.status_code)
            return None

    def get_commit(self, repo, sha):
        """Go to the internet and get a commit; otherwise return nothing."""
        url = '{}/commits/{}'.format(repo, sha)
        vals = self.make_api_request(url, auth=self.auth)
        if vals.status_code == 200:
            payload = vals.json()
            return payload
        else:
            raise ValueError('Could not find commit, status code: {}'.format(vals.status_code))

    def parse_event_page(self, res):
        """From the event page, extract recent pushes (so we can peek into their commits)"""
        commits = []
        if res is not None:
            res_json = res.json()
            pushes = [_ for _ in res_json if _['type'] == 'PushEvent']
            if len(pushes) > 0:
                for p in pushes:
                    for commit in p['payload']['commits']:
                        commits.append({'repo': p['repo']['url'], 'sha': commit['sha']})
        return commits

    def validate_commit(self, payload):
        """Check if a commit contains a file we are looking for."""
        ret_vals = []
        if type(payload) != dict:
            import pdb; pdb.set_trace()
            return
        for item in payload['files']:
            if item.get('raw_url') is None:
                continue
            if is_root_package_json(item.get('raw_url')) or item.get('filename').lower().endswith('requirements.txt'):
                url_info = parse_for_meta(item.get('raw_url'))
                repo_data = {
                    'repo_name': url_info['repo'],
                    'sha': payload.get('sha'),
                    'user': url_info['user'],
                    'repo_type': item.get('filename').lower(),
                    'check_state': 'FOUND',
                    'target_file_url': item.get('raw_url')
                }
                ret_vals.append(repo_data)
        return ret_vals

    def store_commit(self, item):
        """Store the commit in the database."""
        c = RepositoryMoment(**item)
        self.db.add(c)
        try:
            self.db.commit()
        except IntegrityError as err:
            print(err)
            self.db.rollback()
        except SQLAlchemyError as err:
            print(err)
            self.db.rollback()

    def store_dep(self, item):
        """Store the commit in the database."""
        c = Dependency(**item)
        self.db.add(c)
        try:
            self.db.commit()
        except IntegrityError as err:
            print(err)
            self.db.rollback()
        except SQLAlchemyError as err:
            print(err)
            self.db.rollback()

    def get_new_commits_by_file(self):
        """Get the events page, check for pushes and check each push for files we care about."""
        for i in range(0, 10):
            events = self.get_events(page=i)
            if events is not None:
                commits = self.parse_event_page(events)
                for commit in commits:
                    try:
                        commit_metadata = self.get_commit(commit['repo'], commit['sha'])
                    except ValueError as e:
                        print('Unable to get commit: error: {}'.format(e))
                        continue
                    results = self.validate_commit(commit_metadata)
                    if results is not None:
                        for item in results:
                            self.store_commit(item)
        self.etag = None

    def create_db_dependency(self, k, v, item_id, dd=False):
        dep_val = parse_js_dep(k, v)
        dep_val.update({
            'repository_moment': item_id,
            'lang': 'js',
            'is_dev_dep': dd
        })
        return dep_val

    def retrieve_and_parse_database_deps(self):
        js_deps = self.db.query(RepositoryMoment).filter(RepositoryMoment.check_state == 'FOUND') \
                                                 .filter(RepositoryMoment.repo_type == 'package.json')
        if js_deps.count() <= 0:
            return None

        item = js_deps.first()
        package = self.make_request(item.target_file_url)
        if package is not None:
            data = package.json()
            if 'devDependencies' in data:
                for k, v in data['devDependencies'].items():
                    dep = self.create_db_dependency(k, v, item.id, dd=True)
                    self.store_dep(dep)
            if 'dependencies' in data:
                for k, v in data['dependencies'].items():
                    dep = self.create_db_dependency(k, v, item.id, dd=False)
                    self.store_dep(dep)
            item.check_state = 'UPDATED'
            self.db.commit()


def main():
    grabber = GStalker()
    i = 1
    while i is not None:
        grabber.retrieve_and_parse_database_deps()
        for i in range(0, 100):
            grabber.get_new_commits_by_file()


if __name__ == '__main__':
    main()
