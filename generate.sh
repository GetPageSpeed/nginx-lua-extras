#!/bin/bash
set -eo pipefail
set -x
# ensure github api token added
source "${HOME}/.bashrc"
cd "$(dirname "$0")"

git fetch --all
git checkout master

# cleanup gitignored stuff (leftovers of previous jobs maybe)
git clean -fX >/dev/null

# remove spec files for modules no longer built
rm -rf ./*.spec

if [[ -t 1 ]]; then
    bold=$(tput bold)
    normal=$(tput sgr0)
else
    bold=""
    normal=""
fi

for ymlConfig in ./resty/*.yml; do
  echo "${bold}====== Processing $ymlConfig ======${normal}"
  LUA_PKG_NAME="resty-$(basename $ymlConfig .yml)"
  moduleName="lua-${LUA_PKG_NAME}"
  echo "Generating ${moduleName}.spec ...  "
  # generate .spec by feeding module .yml to lastversion, then template result via jinja2cli
  lastversion "${ymlConfig}" --format json  |
    jinja2 -D luapkgname=${LUA_PKG_NAME} --format=json spec.j2 --strict - > ${moduleName}.spec
  echo "Done!"

  printf "Checking with rpmlint ...:  "
  # rpmlint -f ./rpmlint.config ./${moduleName}.spec
done

# remove problematic packages:
# lua-resty-newrelic.src: W: invalid-url Source0: https://github.com/saks/lua-resty-newrelic/archive/v0.01-6/lua-resty-newrelic-v0.01-6.tar.gz HTTP Error 300: Multiple Choices
rm -rf ./lua-resty-newrelic.spec

git add --all .
# at this point we don't know what updated: rpmmacros or spec files, but we check-in all
git commit -m "Updated"
git push --force origin
git checkout master

