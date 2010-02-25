# Copyright (c) 2010 Friedrich Romstedt <www.friedrichromstedt.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Last changed: 2010 Feb 12
# Developed since: Jul 2008
# File version: 0.2.11b

try:
	import matplotlib.cm
except:
	pass
try:
	import numpy
except:
	pass

class Layer:
	def __init__(self):
		self.set_changed()

	def set_changed(self):
		self.changed = True

	def not_changed(self):
		self.changed = False

class Layer2D(Layer):
	def __init__(self,
			x, y,
			yerrors = None, xerrors = None,
			fmt = '+-', fmt_envelope = None,
			color = None,
			x_en = False, y_en = False,
			x_ua = False, y_ua = False,
			envelope = False):
		"""X and Y are the datasets of equal, one-dimensionsional shape.
		All other arguments are optional.  XERRORS and YERRORS specify 
		directly the resp. quantity.  FMT influences plotting format.  
		FMT_ENVELOPE determines plot format of the optional envelope.  
		COLOR is the plot color.  X_EN and Y_EN specify X and Y to be 
		iterables of some enumber class instances (with .value and .error).
		X_UA and Y_UA specify X and Y to be some undarray class instance
		(with .value and .error() methods, yielding the arrays).  ENVELOPE
		turns the envelope on.  Envelope mode requires some y errors and 
		COLOR."""

		Layer.__init__(self)
		self.set_x(x, xerrors, x_en, x_ua)
		self.set_y(y, yerrors, y_en, y_ua)
		self.set_fmt(fmt, fmt_envelope)
		self.set_color(color)
		self.set_envelope(envelope)

	def set_x(self, x, xerrors = None, x_en = False, x_ua = False):
		if x_en:
			self.x = map(lambda en: en.value,x)
			self.xerrors = map(lambda en: en.error,x)
		elif x_ua:
			self.x = x.value
			self.xerrors = x.error()
		else:
			self.x = x
			self.xerrors = xerrors
		self.set_changed()

	def set_y(self, y, yerrors = None, y_en = False, y_ua = False):
		if y_en:
			self.y = map(lambda en: en.value,y)
			self.yerrors = map(lambda en: en.error,y)
		elif y_ua:
			self.y = y.value
			self.yerrors = y.error()
		else:
			self.y = y
			self.yerrors = yerrors
		self.set_changed()

	def set_fmt(self,fmt,fmt_envelope=None):
		if fmt_envelope is None:
			fmt_envelope=fmt
		self.fmt = fmt
		self.fmt_envelope = fmt_envelope
		self.set_changed()

	def set_color(self,color):
		self.color = color
		self.set_changed()

	def set_envelope(self,envelope):
		self.envelope = envelope
		self.set_changed()

class Layer3D(Layer):
	def __init__(self, X, Y, C, alpha = None, shading = None, cm = None,
			vmin = None, vmax = None):
		if alpha is None:
			alpha = 1.0
		if shading is None:
			shading = 'flat'
		if cm is None:
			cm = 'bw'

		Layer.__init__(self)
		self.set_XYC(X, Y, C)
		self.alpha = alpha
		self.shading = shading

		if cm == 'bw':
			self.cm = matplotlib.cm.gray
		else:
			self.cm = matplotlib.cm.jet

		self.set_vlim(vmin, vmax)

	def set_XYC(self, X, Y, C):
		X = numpy.asarray(X)
		Y = numpy.asarray(Y)

		if X.ndim == 1 and Y.ndim == 1:
			xlength = len(X)
			ylength = len(Y)

			X = numpy.asarray([X])
			X = X.repeat(ylength, axis=0)

			Y = numpy.asarray([Y])
			Y = Y.transpose()
			Y = Y.repeat(xlength, axis=1)

		elif X.ndim==2 and Y.ndim==2:
			pass

		else:
			raise ValueError('one- and twodimensional X and Y cannot be mixed')
		
		self.X = X
		self.Y = Y
		self.C = C
		self.set_changed()

	def set_vlim(self, vmin, vmax):
		self.vmin = vmin
		self.vmax = vmax
		self.set_changed()
