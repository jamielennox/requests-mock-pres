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

import logging

import click
import dotenv
import terminaltables

from requests_mock_pres import model


@click.group()
@click.option('-d', '--debug', default=False, is_flag=True)
@click.option('--access-token')
@click.pass_context
def cli(ctx, debug, access_token):
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    print("Access Token is: %s" % access_token)
    ctx.obj['app'] = model.App(access_token=access_token)


@cli.command()
@click.argument('repository')
@click.pass_context
def show(ctx, repository):
    """List the open PRs for a given repository."""
    data = [['ID', 'Title', 'User', 'Status', 'URL']]
    prs = ctx.obj['app'].list_prs(repository)

    for pr in prs:
        data.append([pr.number,
                     pr.title,
                     pr.user,
                     '%d / %d' % (pr.success_count, pr.status_count),
                     pr.url])

    table = terminaltables.AsciiTable(data)
    print(table.table)


def main():
    # load .env file for development variables if available
    dotenv_path = dotenv.find_dotenv()
    if dotenv_path:
        dotenv.load_dotenv(dotenv_path)

    cli(auto_envvar_prefix='RMP', obj={})


if __name__ == '__main__':
    main()
