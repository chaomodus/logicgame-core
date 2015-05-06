#!/bin/sh

find -name '*~' |xargs rm
find -name '*.pyc' |xargs rm
if [ -d html ]; then
    rm -r html
fi
if [ -d build ]; then
    rm -r build
fi
if [ -d logicgamecore.egg-info ]; then
    rm -r logicgamecore.egg-info
fi
if [ -d dist ]; then
    rm -r dist
fi
