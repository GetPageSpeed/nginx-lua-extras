#!/usr/bin/env python3

from github import Github
from github.GithubException import UnknownObjectException, GithubException
import os
import logging as log
from lastversion import lastversion
import yaml
import re

openresty_str = re.compile("OpenResty", re.IGNORECASE)

# search github lua-resty with pagination
# check if repo has got lib/resty dir
# check if got releases

# if fail conditions - add to ignore list

# or using an access token
from github.Repository import Repository

g = Github(os.getenv("GITHUB_API_TOKEN"))
work_dir = os.path.dirname(__file__)

log.basicConfig(level=log.INFO)

repositories = g.search_repositories(query='lua-resty- in:name stars:>=10 archived:false')
repo: Repository
for repo in repositories:
    log.info(f'================= {repo.full_name} =================')
    if not repo.name.startswith('lua-resty-'):
        log.warning('Skipping. Does not start with lua-resty-')
        continue
    if not repo.description:
        log.warning('Skipping. Has no description')
        continue
    module_name = repo.name.replace('lua-resty-', '')
    filename = os.path.join(work_dir, f'resty/{module_name}.yml')
    if os.path.exists(filename):
        log.warning('Skipping. Definition already exists for this name. Likely a less popular fork')
        continue
    try:
        contents = repo.get_contents('lib/resty')
    except (UnknownObjectException, GithubException):
        log.warning(f"Skipping. Has no lib/resty")
        continue

    release = lastversion.latest(repo.full_name, output_format='json')
    if not release:
        log.warning('Skipping. Has no good formal release version')
        continue
    release_tag = release['tag_name']
    release = release['version']
    # there may be no lib/resty at release tag, we don't want stuff like that
    try:
        contents = repo.get_contents('lib/resty', ref=release_tag)
    except (UnknownObjectException, GithubException):
        log.warning(f"Skipping. Has no lib/resty or empty empty at release tag")
        continue

    log.info(f'All checks passed. Adding {repo.full_name} definition yml...')
    log.info(f'Original description: {repo.description}')
    summary = repo.description.replace('ngx_lua', 'nginx-module-lua')
    summary = openresty_str.sub("nginx-module-lua", summary). \
        replace('based on Openresty', ''). \
        replace('nginx lua module', 'nginx-module-lua'). \
        replace('nginx-module-lua / nginx-module-lua', 'nginx-module-lua'). \
        replace('Lua and OpenResty', 'nginx-module-lua'). \
        replace('nginx-module-lua/NGINX', 'nginx-module-lua'). \
        replace('nginx-module-lua/lua', 'nginx-module-lua'). \
        replace('(and nginx-module-lua)', ''). \
        replace('stream-Lua-NGINX-module', 'nginx-module-lua-stream'). \
        replace('I must be crazy trying to', ''). \
        replace('nginx-module-luaJIT', 'nginx-module-lua'). \
        replace(':)', ''). \
        replace(f'{repo.name} -', '')
    summary = summary.replace('nginx-module-lua/nginx-module-lua', 'nginx-module-lua')
    summary = summary.replace('the nginx-module-lua', 'nginx-module-lua')
    summary = summary.replace('nginx-module-lua or nginx-module-lua', 'nginx-module-lua')
    summary = summary.replace('nginx-module-lua/Lua', 'nginx-module-lua')
    summary = summary.replace('Nginx', 'NGINX')
    summary = summary.rstrip('.').strip().rstrip('.')
    summary = summary[:1].upper() + summary[1:]
    log.info(f'Converted summary: {summary}')
    dict_file = {
        'repo': repo.full_name,
        'summary': summary
    }

    with open(filename, 'w', encoding='utf8') as file:
        documents = yaml.dump(dict_file, file)

    log.info('Definition saved!')
