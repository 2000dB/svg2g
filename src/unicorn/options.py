#!/usr/bin/env python

def add_options(options):
    """
    Add options to a optparse options.
    """
    options.add_option('--pen-up-angle',
        action='store',
        type='float',
        dest='pen_up_angle',
        default='50.0',
        help='Pen Up Angle')

    options.add_option('--pen-down-angle',
        action='store',
        type='float',
        dest='pen_down_angle',
        default='30.0',
        help='Pen Down Angle')

    options.add_option('--start-delay',
        action='store', 
        type='float',
        dest='start_delay', 
        default='150.0',
        help='Delay after pen down command before movement in milliseconds')

    options.add_option('--stop-delay',
        action='store',
        type='float',
        dest='stop_delay',
        default='150.0',
        help='Delay after pen up command before movement in milliseconds')

    options.add_option('--xy-feedrate',
        action='store',
        type='float',
        dest='xy_feedrate',
        default='3500.0',
        help='XY axes feedrate in mm/min')

    options.add_option('--z-feedrate',
        action='store',
        type='float',
        dest='z_feedrate',
        default='150.0',
        help='Z axis feedrate in mm/min')

    options.add_option('--z-height',
        action='store',
        type='float',
        dest='z_height',
        default='0.0',
        help='Z axis print height in mm')

    options.add_option('--finished-height',
        action='store',
        type='float',
        dest='finished_height',
        default='0.0',
        help='Z axis height after printing in mm')

    options.add_option('--register-pen',
        action='store',
        type='string',
        dest='register_pen',
        default='true',
        help='Add pen registration check(s)')

    options.add_option('--x-home',
        action='store',
        type='float',
        dest='x_home',
        default='0.0',
        help='Starting X position')

    options.add_option('--y-home',
        action='store',
        type='float',
        dest='y_home',
        default='0.0',
        help='Starting Y position')

    options.add_option('--num-copies',
        action='store',
        type='int',
        dest='num_copies',
        default='1')

    options.add_option('--continuous',
        action='store',
        type='string',
        dest='continuous',
        default='false',
        help='Plot continuously until stopped.')

    options.add_option('--pause-on-layer-change',
        action='store',
        type='string',
        dest='pause_on_layer_change',
        default='false',
        help='Pause on layer changes.')

    options.add_option('--tab',
        action='store',
        type='string',
        dest='tab')
