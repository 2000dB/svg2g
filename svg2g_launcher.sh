#!/usr/bin/env bash

SVG2G="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SVG2G=$SVG2G/src/svg2g.py

$SVG2G --start-delay=100 --stop-delay=100 --xy-feedrate=3000 --y-home=103 --z-home=125 --xoffset=64 --paper-length=100 $1 > $2
