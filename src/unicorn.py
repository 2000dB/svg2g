#!/usr/bin/env python

import optparse
import sys

from lxml import etree

from unicorn.context import GCodeContext
from unicorn.svg_parser import SvgParser

class Unicorn(object):
    def __init__(self):
        self.OptionParser = optparse.OptionParser(usage="usage: %prog [options] SVGfile")

        self.OptionParser.add_option('--pen-up-angle',
            action='store',
            type='float',
            dest='pen_up_angle',
            default='50.0',
            help='Pen Up Angle')

        self.OptionParser.add_option('--pen-down-angle',
            action='store',
            type='float',
            dest='pen_down_angle',
            default='30.0',
            help='Pen Down Angle')

        self.OptionParser.add_option('--start-delay',
            action='store', 
            type='float',
            dest='start_delay', 
            default='150.0',
            help='Delay after pen down command before movement in milliseconds')

        self.OptionParser.add_option('--stop-delay',
            action='store',
            type='float',
            dest='stop_delay',
            default='150.0',
            help='Delay after pen up command before movement in milliseconds')

        self.OptionParser.add_option('--xy-feedrate',
            action='store',
            type='float',
            dest='xy_feedrate',
            default='3500.0',
            help='XY axes feedrate in mm/min')

        self.OptionParser.add_option('--z-feedrate',
            action='store',
            type='float',
            dest='z_feedrate',
            default='150.0',
            help='Z axis feedrate in mm/min')

        self.OptionParser.add_option('--z-height',
            action='store',
            type='float',
            dest='z_height',
            default='0.0',
            help='Z axis print height in mm')

        self.OptionParser.add_option('--finished-height',
            action='store',
            type='float',
            dest='finished_height',
            default='0.0',
            help='Z axis height after printing in mm')

        self.OptionParser.add_option('--register-pen',
            action='store',
            type='string',
            dest='register_pen',
            default='true',
            help='Add pen registration check(s)')

        self.OptionParser.add_option('--x-home',
            action='store',
            type='float',
            dest='x_home',
            default='0.0',
            help='Starting X position')

        self.OptionParser.add_option('--y-home',
            action='store',
            type='float',
            dest='y_home',
            default='0.0',
            help='Starting Y position')

        self.OptionParser.add_option('--num-copies',
            action='store',
            type='int',
            dest='num_copies',
            default='1')

        self.OptionParser.add_option('--continuous',
            action='store',
            type='string',
            dest='continuous',
            default='false',
            help='Plot continuously until stopped.')

        self.OptionParser.add_option('--pause-on-layer-change',
            action='store',
            type='string',
            dest='pause_on_layer_change',
            default='false',
            help='Pause on layer changes.')

        self.OptionParser.add_option('--tab',
            action='store',
            type='string',
            dest='tab')

        self.options, self.args = self.OptionParser.parse_args(sys.argv[1:])

    def output(self):
        self.context.generate()

    def parse(self, path):
        try:
            stream = open(path, 'r')
        except:
            stream = sys.stdin

        document = etree.parse(stream)

        stream.close()

        return document

    def effect(self):
        self.context = GCodeContext(self.options)

        document = self.parse(sys.argv[-1]) 

        parser = SvgParser(document.getroot(), self.options.pause_on_layer_change)
        parser.parse()

        for entity in parser.entities:
            entity.get_gcode(self.context)

        self.context.generate()

if __name__ == '__main__': 
    e = Unicorn()
    e.effect()
