#!/bin/sh
git config --global user.email "yangxinhust@hotmail.com"
git config --global user.name "Hsiny"
git add -f .
git remote rm origin
git remote add origin https://Hsiny:${TT}@github.com/Hsiny/Shadowrocket-Config.git
git add -A
git commit -m "Dayly Update $TRAVIS_BUILD_NUMBER pushed [skip ci] "
git push origin master
echo -e "Done\n ${TT}"