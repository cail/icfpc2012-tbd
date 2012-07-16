#!/bin/sh
rm -rf build
mkdir build
cp -r production data build/src
cp install lifter README PACKAGES-TESTING build/
cp pypy-1.9-linux.tar.bz2 build/
(cd build && tar -czf ../icfp-96269702.tgz *)
cp -f icfp-*.tgz /media/sf_ICFPC
