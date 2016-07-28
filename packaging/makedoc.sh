#!/bin/bash

gettools="yes" # if set to yes downloads the tools required
setup="yes" # if set to yes populates library folder
buildoc="yes" # if set to yes builds the deb files
cleanup="yes" # if set to yes cleans up build files
pkgfiles=( "build" "changes" "deb" "dsc" "tar.xz" )

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential debhelper devscripts dh-make dh-python
    sudo apt-get install python-mock python-sphinx python-sphinx-rtd-theme python-all python-setuptools python3-all python3-setuptools
fi

if [ $setup == "yes" ]; then
    rm -R ../library/build ../library/debian &> /dev/null
    cp -R ./debian ../library/ && cp -R ../sphinx ../library/doc
fi

cd ../library

if [ $buildoc == "yes" ]; then
    debuild
    for file in ${pkgfiles[@]}; do
        rm ../*.$file &> /dev/null
    done
    rm -R ../documentation/html &> /dev/null
    cp -R ./build/sphinx/html ../documentation
fi

if [ $cleanup == "yes" ]; then
    debuild clean
    rm -R ./build ./debian ./doc &> /dev/null
fi

exit 0
