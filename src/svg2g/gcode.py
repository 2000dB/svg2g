#!/usr/bin/env python

import sys
import re

class GCodeBuilder:
    """
    Build a GCode instruction set.
    """
    def __init__(self, options):
        self.codes = []
        self.config = vars(options)
        self.drawing = False
        self.last = None
        self.end_paper_to_feed = 0
        
    def preamble(self):
        return [
            '(setup)',
            # if config requires homing
            'G28 (home axes)',
            'G1 F%(homing_feedrate)0.2F' % self.config,
            'M83 (Relative E axis - in our case the paper feed return)',
            'G92 X%(x_offset).2f' % self.config,
            'G1 X0.0 E%(x_offset).2f' % self.config,
            'G1 E%(x_offset)2.f (just for safety, keep spooling)' % self.config,
            'G92 X%(x_home).2f Y%(y_home).2f Z%(z_home).2f (set home coordinates)' % (self.config),
            'G1 X0 Y0 (go to 0 position for drawing since the limit switches are currently set to be at the max)',
            'G92 X0 Y0',
            'G1 F%(xy_feedrate)0.2F' % self.config,
            '(/setup done, can now draw)',
            ''
        ]

    def postscript(self):
        return [
            '',
            '(end of drawing)',
            'G1 F%(homing_feedrate).2f' % self.config,
            'G1 X%.2f' % self.end_paper_to_feed,
            # 'G1 X0.0',
            # 'G1 X%(x_offset).2f' % self.config,
            # 'G91',
            # 'G1 X%(paper_length).2f' % self.config,
            'G90'
            'G1 Y%(y_home)0.2f Z0 (go home and cut paper)' % self.config,
            'G1 Z%(z_home)0.2f' % self.config,
            '(/done)',
            ''
        ]

    def registration(self):
        return [
            '',
            '(registration)',
            # Lower pen at the bottom margin, raise, move to top margin and lower again. Go back to 0
            '(/registration)'
        ]

    def sheet_header(self):
        return [
            '(sheet header)',
            'G92 X%(x_home).2f Y%(y_home).2f Z%(z_home).2f (you are here)' % self.config,
        ]

        self.sheet_header.append('(/sheet header)')

    def sheet_footer(self):
        return[
        ]
    
    def loop_forever(self):
        return [
            'M30 (Plot again?)'
        ]

    def start(self):
        """
        Start drawing a shape
        """
        self.codes.append('(lower pen)')
        self.codes.append('M5 M400 M3 S100')
        self.codes.append('G4 P%(stop_delay).2f' % self.config)
        self.drawing = True

    def stop(self):
        """
        Stop drawing a shape
        """
        self.codes.append('(raise pen)')
        self.codes.append('M3 S100 M400 M5') 
        self.codes.append('G4 P%(stop_delay).2f' % self.config)
        self.drawing = False

    def go_to_point(self, x, y, stop=False):
        """
        Move the print head to a certain point.
        """
        if self.last == (x,y):
            return

        if stop:
            return
        else:
            if self.drawing: 
                self.stop();

            if self.last:
                distX = abs(self.last[0] - x)
            else:
                distX = 0.0
            self.codes.append('G1 X%0.2f Y%0.2f E%0.2f F%0.2f' % (x, y, distX, self.config['xy_feedrate']))

        self.last = (x, y)

    def draw_to_point(self, x, y):
        """
        Draw to a certain point.
        """
        if self.last == (x, y):
            return

        if self.drawing == False:
            self.start()

        distX = abs(self.last[0] - x)
            
        self.codes.append('G1 X%0.2f Y%0.2f E%0.2f F%0.2f' % (x, y, distX, self.config['xy_feedrate']))

        self.last = (x, y)

    def label(self, text):
        """
        Write a text label/comment into the output.
        """
        self.codes.append('(' + text + ')')

    def draw_polyline(self, points):
        """
        Draw a polyline (series of points).
        """
        start = points[0]

        self.go_to_point(start[0],start[1])
        self.start()

        for point in points[1:]:
            self.draw_to_point(point[0],point[1])
            self.last = point

        self.stop()

    def change_layer(self, name):
        """
        Change layer being drawn.
        """
        if self.config['pause_on_layer_change']:
            self.codes.append('M01 (Plotting layer "%s")' % name)

    def build(self):
        """
        Build complete GCode and return as string. 
        """
        commands = []

        commands.extend(self.preamble())

        if (self.config['num_copies'] > 1):
            commands.extend(self.sheet_header())
        
        if self.config['register_pen'] == 'true':
            commands.extend(self.registration())
        
        commands.extend(self.codes)

        # Get the last command, figure out what absolute X we're at
        # last_x = 0
        # for i in reversed(commands):
        #     if 'X' in i:
        #         g = re.search(r"(?<=X)[^}]\d+\.\d+", i)
        #         if g:
        #             last_x = float(g.group())
        #         break
            
        self.end_paper_to_feed = self.config['x_offset'] + self.config['paper_length']

        if (self.config['num_copies'] > 1):
            commands.extend(self.sheet_footer())
            commands.extend(self.postscript())
            commands = commands * self.config['num_copies']
        else:
            commands.extend(self.postscript())

        return '\n'.join(commands)
