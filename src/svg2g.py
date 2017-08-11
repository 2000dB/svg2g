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

        self.OptionParser.add_option('--xoffset',
            action='store',
            type='float',
            dest='x_offset',
            default='64.0',
            help='X Offset: Offset in mm between the paper cutter and where the paper should at the start of the writing process.')

        self.OptionParser.add_option('--paper-length',
            action='store',
            type='float',
            dest='paper_length',
            default='100.0',
            help='Final length of the paper to be cut in mm')

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

        self.OptionParser.add_option('--homing-feedrate',
            action='store',
            type='float',
            dest='homing_feedrate',
            default='1000.0',
            help='Feedrate used when doing positioning movement')

        self.OptionParser.add_option('--x-home',
            action='store',
            type='float',
            dest='x_home',
            default='0.0',
            help='Should be left as 0 for now')

        self.OptionParser.add_option('--z-home',
            action='store',
            type='float',
            dest='z_home',
            default='0.0',
            help='Distance between the microswitch and where the paper cutter should end its movement')

        self.OptionParser.add_option('--y-home',
            action='store',
            type='float',
            dest='y_home',
            default='0.0',
            help='Distance between the microswitch and the 0 point, which should be at the very edge of the paper')

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

        output = self.gcode.build()

        sys.stdout.write(output)

if __name__ == '__main__': 
    svg2g = Svg2G()
    svg2g.run()
