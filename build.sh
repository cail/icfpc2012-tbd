#!/bin/sh
rm -rf build
mkdir build
cp -r production build/src
cp install lifter README PACKAGES-TESTING build/