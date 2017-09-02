#!/bin/sh
git add -f .
git remote rm origin
git remote add origin https://Hsiny:a812f841fdcd8dca9576519e2cae32da538e3d38@github.com/Hsiny/Shadowrocket-Config.git
git add -A
git commit -m "Dayly Update $TRAVIS_BUILD_NUMBER pushed [skip ci] "
git push -fq origin master
echo -e "Done\n"