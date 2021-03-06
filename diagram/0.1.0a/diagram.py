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

import layers
import matplotlib.figure as mpl_figure
import matplotlib.backends.backend_agg as mpl_backend_agg
import Image
import matplotlib.backends.backend_ps as mpl_backend_ps

papersize=mpl_backend_ps.papersize

class Diagram:
	def __init__(self,left=0.2,bottom=0.2,right=0.8,top=0.8):
		self.layers=[]
		self.drawn_layers=[]

		self.figure=mpl_figure.Figure(figsize=(0,0),frameon=False)
		self.figure.hold(True)

		self.axes=self.figure.add_axes((left,bottom,right-left,top-bottom))
	def add_layer(self,layer):
		self.layers.append(layer)
	
	def render_to_axes(self,axes):
		for layer in self.layers:
			if layer not in self.drawn_layers:
				if isinstance(layer,layers.Layer2D):
					axes.errorbar(
							x=layer.x,
							y=layer.y,
							xerr=layer.xerrors,
							yerr=layer.yerrors,
							fmt=layer.fmt)
				elif isinstance(layer,layers.Layer3D):
					axes.pcolor(
							layer.X,
							layer.Y,
							layer.C,
							alpha=layer.alpha,
							shading=layer.shading)
			self.drawn_layers.append(layer)
	def render(self):
		self.render_to_axes(self.axes)

	def render_to_image(self,shape):
		self.render()

		dpi=self.figure.dpi.get()
		self.figure.set_figsize_inches(shape[0]/dpi,shape[1]/dpi)

		agg_figure_container=mpl_backend_agg.FigureCanvasAgg(self.figure)
		agg_figure_container.draw()
		image_string=agg_figure_container.tostring_rgb()

		image=Image.fromstring("RGB",shape,image_string)
		return image
	
	def render_to_ps(self,shape,file):
		self.render()

		self.figure.set_figsize_inches(shape[0],shape[1])

		ps_figure_container=mpl_backend_ps.FigureCanvasPS(self.figure)
		ps_figure_container.print_figure(
				outfile=file,
				dpi=self.figure.dpi.get())
