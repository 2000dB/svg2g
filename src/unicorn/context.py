#!/usr/bin/env python

import sys

class GCodeConfig(dict):
    """
    Dictionary wrapper around required GCode configuration.
    """
    def __init__(self, xy_feedrate, z_feedrate, start_delay, stop_delay, pen_up_angle, pen_down_angle, z_height, finished_height, x_home, y_home, register_pen, num_pages, continuous, filename):
        self['xy_feedrate'] = xy_feedrate
        self['z_feedrate'] = z_feedrate
        self['start_delay'] = start_delay
        self['stop_delay'] = stop_delay
        self['pen_up_angle'] = pen_up_angle
        self['pen_down_angle'] = pen_down_angle
        self['z_height'] = z_height
        self['finished_height'] = finished_height
        self['x_home'] = x_home
        self['y_home'] = y_home
        self['register_pen'] = register_pen
        self['num_pages'] = num_pages
        self['continuous'] = continuous
        self['filename'] = filename

class GCodeContext:
    def __init__(self, config):
        self.config = config
        self.drawing = False
        self.last = None

        self.preamble = [
            '(preamble)'
            '(Scribbled version of %(filename)s @ %(xy_feedrate).2f)' % self.config,
            '( %s )' % ' '.join(sys.argv),
            'G21 (metric ftw)',
            'G90 (absolute mode)',
            'G92 X%(x_home).2f Y%(y_home).2f Z%(z_height).2f (you are here)' % self.config,
            '(/preamble)'
        ]

        self.postscript = [
            '(postscript)',
            'M300 S%(pen_up_angle)0.2F (pen up)' % self.config,
            'G4 P%(stop_delay)d (wait %(stop_delay)dms)' % self.config,
            'M300 S255 (turn off servo)',
            'G1 X0 Y0 F%(xy_feedrate)0.2F' % self.config,
            'G1 Z%(finished_height)0.2F F%(z_feedrate)0.2F (go up to finished level)' % self.config,
            'G1 X%(x_home)0.2F Y%(y_home)0.2F F%(xy_feedrate)0.2F (go home)' % (self.config),
            'M18 (drives off)',
            '(/postscript)'
        ]

        self.registration = [
            '(registration)',
            'M300 S%(pen_down_angle)d (pen down)' % self.config,
            'G4 P%(start_delay)d (wait %(start_delay)dms)' % self.config,
            'M300 S%(pen_up_angle)d (pen up)' % self.config,
            'G4 P%(stop_delay)d (wait %(stop_delay)dms)' % self.config,
            'M18 (disengage drives)',
            'M01 (Was registration test successful?)',
            'M17 (engage drives if YES, and continue)',
            '(/registration)'
        ]

        self.sheet_header = [
            '(sheet header)',
            'G92 X%(x_home).2f Y%(y_home).2f Z%(z_height).2f (you are here)' % self.config,
        ]

        if self.config['register_pen'] == 'true':
            self.sheet_header.extend(self.registration)

        self.sheet_header.append('(/sheet header)')

        self.sheet_footer = [
            '(sheet footer)',
            'M300 S%(pen_up_angle)d (pen up)' % self.config,
            'G4 P%(stop_delay)d (wait %(stop_delay)dms)' % self.config,
            'G91 (relative mode)',
            'G0 Z15 F%(z_feedrate)0.2f' % self.config,
            'G90 (absolute mode)',
            'G0 X%(x_home)0.2f Y%(y_home)0.2f F%(xy_feedrate)0.2f' % self.config,
            'M01 (Have you retrieved the print?)',
            '(machine halts until "okay")',
            'G4 P%(start_delay)d (wait %(start_delay)dms)' % self.config,
            'G91 (relative mode)',
            'G0 Z-15 F%(z_feedrate)0.2f (return to start position of current sheet)' % self.config,
            'G0 Z-0.01 F%(z_feedrate)0.2f (move down one sheet)' % self.config,
            'G90 (absolute mode)',
            'M18 (disengage drives)',
            '(/sheet footer)',
        ]

        self.loop_forever = [
            'M30 (Plot again?)'
        ]

        self.codes = []

    def start(self):
        """
        Start drawing.
        """
        self.codes.append('M300 S%(pen_down_angle)0.2F (pen down)' % self.config)
        self.codes.append('G4 P%(start_delay)d (wait %(start_delay)dms)' % self.config)
        self.drawing = True

    def stop(self):
        """
        Stop drawing.
        """
        self.codes.append('M300 S%(pen_up_angle)0.2F (pen up)' % self.config)
        self.codes.append('G4 P%(stop_delay)d (wait %(stop_delay)dms)' % self.config)
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

            self.codes.append('G1 X%.2f Y%.2f F%.2f' % (x, y, self.config.xy_feedrate))

        self.last = (x, y)

    def draw_to_point(self, x, y):
        """
        Draw to a certain point.
        """
        if self.last == (x, y):
            return

        if self.drawing == False:
            self.start()

        self.codes.append('G1 X%0.2f Y%0.2f F%0.2f' % (x, y, self.config.xy_feedrate))

        self.last = (x, y)

    def generate(self):
        """
        Output compiled Godee to console. 
        """
        if self.config['continuous'] == 'true':
            self.config['num_pages'] = 1

        codesets = [self.preamble]

        if (self.config['continuous'] == 'true' or self.config['num_pages'] > 1):
            codesets.append(self.sheet_header)
        elif self.config['register_pen'] == 'true':
            codesets.append(self.registration)
        
        codesets.append(self.codes)
        
        if (self.config['continuous'] == 'true' or self.config['num_pages'] > 1):
            codesets.append(self.sheet_footer)

        if self.config['continuous'] == 'true':
            codesets.append(self.loop_forever)

            for codeset in codesets:
                for line in codeset:
                    print line
        else:
            for p in range(0, self.config['num_pages']):
                for codeset in codesets:
                    for line in codeset:
                        print line

                for line in self.postscript:
                    print line


