#!/usr/bin/env python

"""
This module contains format agnostic entity types.
"""

from math import cos, sin

class Entity(object):
    """
    Base class for an entity.
    """
    def __init__(self):
        pass

	def get_gcode(self,context):
        """
        Emit GCode for drawing this entity.
        """
        #raise NotImplementedError()
		return 'NIE'

class Line(Entity):
    """
    A line.
    """
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

	def __str__(self):
		return 'Line from [%.2f, %.2f] to [%.2f, %.2f]' % (self.start_x, self.start_y, self.end_x, self.end_y)

	def get_gcode(self, context):
		context.codes.append('(' + str(self) + ')')
		context.go_to_point(self.start_x, self.start_y)
		context.draw_to_point(self.end_x, self.end_y)
		context.codes.append('(/line)')

class Circle(Entity):
    """
    A circle.
    """
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

	def __str__(self):
		return 'Circle at [%.2f, %.2f] with radius %.2f' % (self.center_x, self.center_y, self.radius)

	def get_gcode(self, context):
		"""
        Emit gcode for drawing arc
        """
		start_x = self.center_x - self.radius
        start_y = self.center_y

		arc_code = 'G3 I%.2f J0 F%.2f' % (self.radius, context.config['xy_feedrate'])

		context.codes.append('(' + str(self) + ')')
		context.go_to_point(start_x, start_y)
		context.start()
		context.codes.append(arc_code)
		context.stop()
		context.codes.append('(/circle)')

class Arc(Entity):
    """
    An arc.
    """
    def __init__(self, center_x, center_y, radius, start_angle, end_angle):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

	def __str__(self):
		return 'Arc at [%.2f, %.2f] with radius %.2f, from %.2f to %.2f' % (self.center_x, self.center_y, self.radius, self.start_angle, self.end_angle)

	def find_point(self, proportion):
		"""
        Find point at the given proportion along the arc.
        """
		delta = self.end_angle - self.start_angle
		angle = self.start_angle + delta * proportion
		
		return (self.center_x + self.radius * cos(angle), self.center_y + self.radius * sin(angle))

	def get_gcode(self, context):
		"""
        Emit gcode for drawing arc
        """
		start_x, start_y = self.find_point(0)
		end_x, end_y = self.find_point(1)
		delta = self.end_angle - self.start_angle

        # TODO: huh?
		if (delta < 0):
			arc_code = 'G3'
		else:
			arc_code = 'G3'

		arc_code = arc_code + ' X%.2f Y%.2f I%.2f J%.2f F%.2f' % (end_x, end_y, self.center_x - start_y, self.center_y - start_y, context.config['xy_feedrate'])

		context.codes.append('(' + str(self) + ')')
		context.go_to_point(start_x, start_y)
		context.last = end
		context.start()
		context.codes.append(arc_code)
		context.stop()
		context.codes.append('(/arc)')
        
class Ellipse(Entity):
    """
    An ellipse.
    """
    def __str__(self):
		return 'Ellipse at [%.2f, %.2f], major [%.2f, %.2f], minor/major %.2f' + ' start %.2f end %.2f' % \
		(self.center[0], self.center[1], self.major[0], self.major[1], self.minor_to_major, self.start_param, self.end_param)

    def get_gcode(self, context):
        # TODO
        return 'NIE'

class PolyLine(Entity):
    """
    A multi-segment line.
    """
    def __init__(self):
        self.segments = []

	def __str__(self):
		return 'Polyline consisting of %d segments.' % len(self.segments)

	def get_gcode(self,context):
		"""
        Emit gcode for drawing polyline
        """
		for points in self.segments:
			start = points[0]

			context.codes.append('(' + str(self) + ')')
			context.go_to_point(start[0],start[1])
			context.start()

			for point in points[1:]:
				context.draw_to_point(point[0],point[1])
				context.last = point

			context.stop()
			context.codes.append('')

