#!/bin/sh

setup_git() {
  git config --global user.email "yangxinhust@hotmail.com"
  git config --global user.name "Hayden"
}

commit_website_files() {
  git add -A
  git commit --message "Daily Update [skip travis]"
}

upload_files() {
  git remote rm origin
  git remote add origin https://${GH_TOKEN}@github.com/Hsiny/Shadowrocket-Config.git > /dev/null 2>&1
  git push --quiet --set-upstream origin master
}

setup_git
commit_website_files
upload_files