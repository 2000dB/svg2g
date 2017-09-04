#!/usr/bin/env bash

SVG2G="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SVG2G=$SVG2G/src/svg2g.py

marginX=$3
paperLength=$4
echo $4
# Distance between the blade cutter and the pen is 94mm so a 64mm xoffset = margin of 30mm
$SVG2G --start-delay=100 --stop-delay=100 --xy-feedrate=3000 --y-home=103 --z-home=125 --xoffset=$3 --paper-length=$4 $1 > $2
