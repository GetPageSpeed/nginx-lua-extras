#!/bin/bash
set -eo pipefail
set -x
# ensure github api token added
source ~/.bashrc
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

for ymlConfig in ./resty/*.yml
do
  echo "${bold}====== Processing $ymlConfig ======${normal}"
  moduleName="lua-resty-$(basename $ymlConfig .yml)"
  printf "Generating ${moduleName}.spec ...  "
  # generate .spec by feeding module .yml to lastversion, then template result via jinja2cli
  lastversion ${ymlConfig} --format json  |
    jinja2 -D name=${moduleName} --format=json spec.j2 --strict - > ${moduleName}.spec
  echo "Done!"

  printf "Checking with rpmlint ...:  "
  # rpmlint -f ./rpmlint.config ./${moduleName}.spec
done

git add --all .
# at this point we don't know what updated: rpmmacros or spec files, but we check-in all
git commit -m "Updated"
git push --force origin
git checkout master

