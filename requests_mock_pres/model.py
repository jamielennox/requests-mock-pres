# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import operator
import platform

import requests


USER_AGENT = 'requests-mock-pres/0.1 %s %s/%s' % (
    requests.utils.default_user_agent(),
    platform.python_implementation(), platform.python_version())


def _url(*args):
    return 'https://api.github.com/%s' % '/'.join(a.strip('/') for a in args)


class PR(object):

    number = None
    title = None
    user = None
    url = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class App(object):

    def __init__(self, access_token=None, session=None):
        self.session = session or requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT
        self.session.headers['Accept'] = 'application/vnd.github.v3+json'

        if access_token:
            self.session.headers['Authorization'] = 'token %s' % access_token

    def list_prs(self, repo: str):
        prs_resp = self.session.get(_url('repos', repo, 'pulls'))
        prs_resp.raise_for_status()

        data = []

        # pprint.pprint(prs_resp.json()[0])

        for pr in prs_resp.json():
            status_resp = self.session.get(pr['statuses_url'])
            status_resp.raise_for_status()
            status_json = status_resp.json()

            success = [s['context']
                       for s in status_json
                       if s['state'] == 'success']

            # pprint.pprint(status_resp.json())

            data.append(PR(number=pr['number'],
                           title=pr['title'],
                           user=pr['user']['login'],
                           status_count=len(status_json),
                           success_count=len(success),
                           url=pr['html_url']))

        data.sort(key=operator.attrgetter('number'))
        return data

    def merge(self, repo: str, pr: str):
        pass
