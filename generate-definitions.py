#!/usr/bin/env python3
import configparser
from github import Github
from github.GithubException import UnknownObjectException, GithubException
import os
from lastversion import lastversion
import yaml
import re
import logging


def setup_logging(level=logging.INFO):
    """
    Setup logging configuration for CLI applications.
    """
    logger = logging.getLogger()  # root logger
    logger.setLevel(level)  # or whatever minimum level you want

    # Create a handler that writes log messages to stderr, with level
    # WARNING and above
    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    err_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(err_handler)

    return logger


log = setup_logging()
openresty_str = re.compile("OpenResty", re.IGNORECASE)

# search github lua-resty with pagination
# check if repo has got lib/resty dir
# check if got releases

# if fail conditions - add to ignore list

# or using an access token
from github.Repository import Repository

g = Github(os.getenv("GITHUB_API_TOKEN"))
work_dir = os.path.dirname(__file__)

disabled_repos = {
    'saks/lua-resty-newrelic': 'Downloading release .tar.gz results in a HTTP Error 300: Multiple Choices'
}

repositories = g.search_repositories(query='lua-resty- in:name stars:>=10 archived:false', sort='stars')
repo: Repository
for repo in repositories:
    log.info(f'================= {repo.full_name} =================')
    if not repo.name.startswith('lua-resty-'):
        log.warning('Skipping. Does not start with lua-resty-')
        continue
    if not repo.description:
        log.warning('Skipping. Has no description')
        continue
    if repo.full_name in disabled_repos:
        log.warning(f"Skipping a bad repo {repo.full_name} because it usually errors. Reason: {disabled_repos[repo.full_name]}")
        continue
    module_name = repo.name.replace('lua-resty-', '')
    filename = os.path.join(work_dir, f'resty/{module_name}.yml')
    # If module file has been created during this launch (e.g. author1/repo1 and author2/repo1 have same name)
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

    try:
        contents = repo.get_contents('dist.ini')
    except (UnknownObjectException, GithubException):
        log.warning(f"Has no dist.ini")
    else:
        contents = '[config]\n' + contents.decoded_content.decode("utf-8")
        config = configparser.ConfigParser()
        config.read_string(contents)
        print(contents)
        requires = config.get('config', 'requires', fallback=None)
        if requires:
            # replace bad versions like 0.08 with 0.8
            requires = re.sub(r'0\.0(\d)', r"0.\1", requires)
            requires = requires.split(',')
            requires_found = []
            lib_requires_found = []
            for r in requires:
                parts = r.split('/')
                r = parts[-1].strip()
                if r.startswith('lua-resty-'):
                    lib_requires_found.append(r.replace('lua-', ''))
            print(requires)
            print(lib_requires_found)
            if lib_requires_found:
                dict_file['lib_requires'] = lib_requires_found

    with open(filename, 'w', encoding='utf8') as file:
        documents = yaml.dump(dict_file, file)

    log.info('Definition saved!')
