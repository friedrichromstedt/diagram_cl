# Maintainer: Friedrich Romstedt <friedrichromstedt@gmail.com>
# Copyright 2008 Friedrich Romstedt
#    This file is part of diagram.
#
#    Diagram is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Diagram is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Diagram.  If not, see <http://www.gnu.org/licenses/>.
# $Last changed: 2008 Jul 31$
# Developed since: Jul 2008
# Version: 0.1.0a

class Layer2D:
	def __init__(self,x,y,yerrors=None,xerrors=None,fmt='+-'):
		self.x=x
		self.y=y
		self.xerrors=xerrors
		self.yerrors=yerrors
		self.fmt=fmt

class Layer3D:
	def __init__(self,X,Y,C,alpha=1.0,shading='flat'):
		self.X=X
		self.Y=Y
		self.C=C
		self.alpha=alpha
		self.shading=shading
