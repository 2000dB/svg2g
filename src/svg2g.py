#!/usr/bin/env python

import optparse
import sys

from lxml import etree

from svg2g.gcode import GCodeBuilder
from svg2g.svg import SvgLayerChange, SvgParser, SvgPath

class Svg2G(object):
    def __init__(self):
        """
        Setup GCode writer and SVG parser.
        """
        self.get_options()

        self.gcode = GCodeBuilder(self.options)
        
        # TODO: use actual argument
        document = self.parse_xml(sys.argv[-1]) 
        
        self.parser = SvgParser(document.getroot())

    def get_options(self):
        """
        Get options from the command line.
        """
        self.OptionParser = optparse.OptionParser(usage='usage: %prog [options] input.svg')

        self.OptionParser.add_option('--pen-up-angle',
            action='store',
            type='float',
            dest='pen_up_angle',
            default='50.0',
            help='Pen up angle')

        self.OptionParser.add_option('--pen-down-angle',
            action='store',
            type='float',
            dest='pen_down_angle',
            default='30.0',
            help='Pen down angle')

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
            help='XY axes feedrate in millimeters per minute')

        self.OptionParser.add_option('--z-feedrate',
            action='store',
            type='float',
            dest='z_feedrate',
            default='150.0',
            help='Z axis feedrate in millimeters per minute')

        self.OptionParser.add_option('--z-height',
            action='store',
            type='float',
            dest='z_height',
            default='0.0',
            help='Z axis print height in millimeters')

        self.OptionParser.add_option('--finished-height',
            action='store',
            type='float',
            dest='finished_height',
            default='0.0',
            help='Z axis height after printing in millimeters')

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
            default='1',
            help='Number of times to repeat the GCode in the output.')

        self.OptionParser.add_option('--pause-on-layer-change',
            action='store',
            type='string',
            dest='pause_on_layer_change',
            default='false',
            help='Pause on layer changes')

        # Option required for inkscape support
        self.OptionParser.add_option('--tab',
            action='store',
            type='string',
            dest='tag',
            help='Ignored (required for Inkscape support)')

        self.options, self.args = self.OptionParser.parse_args(sys.argv[1:])

    def parse_xml(self, path):
        """
        Parse the XML input.
        """
        try:
            stream = open(path, 'r')
        except:
            stream = sys.stdin

        document = etree.parse(stream)

        stream.close()

        return document

    def process_svg_entity(self, svg_entity):
        """
        Generate GCode for a given SVG entity.
        """
        if isinstance(svg_entity, SvgPath):
            len_segments = len(svg_entity.segments)

            for i, points in enumerate(svg_entity.segments):
                self.gcode.label('Polyline segment %i/%i' % (i + 1, len_segments))
                self.gcode.draw_polyline(points)
        elif isinstance(svg_entity, SvgLayerChange):
            self.gcode.change_layer(svg_entity.layer_name)

    def run(self):
        """
        Execute the parser and generate the GCode.
        """
        self.parser.parse()

        map(self.process_svg_entity, self.parser.entities)

        sys.stdout.write(self.gcode.build())

if __name__ == '__main__': 
    svg2g = Svg2G()
    svg2g.run()
