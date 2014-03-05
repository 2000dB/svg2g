svg2g: Convert SVG to GCode 
===========================

**NOTE:** This code is nearly-complete rewrite of [MakerBot Unicorn G-Code Output for Inkscape](http://github.com/martymcguire/inkscape-unicorn) by [Marty McGuire](http://github.com/martymcguire). It continues to support Inkscape, but has been refactored to also work on the command line.

Using on the command line
=========================

See `test.sh` for a temporary example.

Install to Inkscape
===================

Copy the contents of `src/` to your Inkscape `extensions/` folder.

Typical locations include:

* OSX - `/Applications/Inkscape.app/Contents/Resources/extensions`
* Linux - `/usr/share/inkscape/extensions`
* Windows - `C:\Program Files\Inkscape\share\extensions`

LICENSE
=======

This source is modified and released under the terms of the GPLv2 open source license. See `LICENSE` for details. 

Some source files in the `src/lib` directory are pulled from the [Inkscape](http://www.inkscape.org/) project. See their headers for individual specific license details.

