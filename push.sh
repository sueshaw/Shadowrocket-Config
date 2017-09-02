#!/bin/sh
git add -f .
git remote rm origin
git remote add origin https://Hsiny:$GH_TOKEN@github.com/Hsiny/Shadowrocket-Config.git
git add -f .
git commit -m "Dayly Update $TRAVIS_BUILD_NUMBER pushed [skip ci] "
git push -fq origin master > /dev/null
echo -e "Done\n"