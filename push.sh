#!/bin/sh
git config --global user.email "yangxinhust@hotmail.com"
git config --global user.name "Hsiny"
git add -f .
git remote rm origin
git remote add origin https://Hsiny:b49d0b6de1032727d0738c108f6fdb1df24691d8@github.com/Hsiny/Shadowrocket-Config.git
git add -A
git commit -m "Dayly Update $TRAVIS_BUILD_NUMBER pushed [skip ci] "
git push -fq origin master
echo -e "Done\n"