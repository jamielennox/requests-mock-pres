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

import os

import betamax
import requests

from requests_mock_pres import app
import tests.base

# most betamax configuration is global, we can just set it here
config = betamax.Betamax.configure()
config.cassette_library_dir = os.path.join('tests', 'integration', 'cassettes')

# allow setting the record mode from environment variable.
# options are: all, new_episodes, none, once
# see: http://betamax.readthedocs.io/en/latest/record_modes.html
record_mode = os.environ.get('RMP_RECORD_MODE', 'none')
config.default_cassette_options['record_mode'] = record_mode


class TestCase(tests.base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        # create a session, create the betamax recorder with it and start it
        self.session = requests.Session()
        self.recorder = betamax.Betamax(session=self.session)
        self.recorder.use_cassette(self.id())
        self.recorder.start()
        self.addCleanup(self.recorder.stop)

        # create the app, using the betamax session
        self.app = app.App(self.session)

    def test_one(self):
        self.assertTrue(False)
