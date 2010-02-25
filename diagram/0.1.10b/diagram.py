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
# $Last changed: 2008 Nov 18$
# Developed since: Jul 2008
# File Version: 0.1.10b

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

		self.set_title("")
		self.set_xlabel("")
		self.set_ylabel("")

		self.set_autoscale_on(True)

	def add_layer(self,layer):
		self.layers.append(layer)

	def set_title(self,title):
		self.axes.set_title(title)
		self.title=title

	def set_xlabel(self,xlabel):
		self.axes.set_xlabel(xlabel)
		self.xlabel=xlabel

	def set_ylabel(self,ylabel):
		self.axes.set_ylabel(ylabel)
		self.ylabel=ylabel

	def set_xlim(self,lim):
		self.xlim=lim
		if lim is not None:
			self.set_autoscale_on(False)
			self.axes.set_xlim(lim)

	def set_ylim(self,lim):
		self.ylim=lim
		if lim is not None:
			self.set_autoscale_on(False)
			self.axes.set_ylim(lim)

	def set_autoscale_on(self,autoscale_on):
		self.autoscale_on=autoscale_on
		self.axes.set_autoscale_on(autoscale_on)
		if autoscale_on:
			self.set_xlim(None)
			self.set_ylim(None)
			self.axes.autoscale_view()

	def reset(self):
		self.axes.clear()
		self.set_title(self.title)
		self.set_xlabel(self.xlabel)
		self.set_ylabel(self.ylabel)
		self.set_xlim(self.xlim)
		self.set_ylim(self.ylim)
		self.drawn_layers=[]

	def clear(self):
		self.set_xlim(None)
		self.set_ylim(None)
		self.set_autoscale_on(True)
		self.reset()
		self.layers=[]
	
	def render(self):
		reset_needed=False
		for layer in self.layers:
			if layer.changed and layer in self.drawn_layers:
				reset_needed=True
		if reset_needed:
			self.reset()
		for layer in self.layers:
			if layer not in self.drawn_layers:
				if isinstance(layer,layers.Layer2D):
					if layer.color is None:
						self.axes.errorbar(
								x=layer.x,
								y=layer.y,
								xerr=layer.xerrors,
								yerr=layer.yerrors,
								fmt=layer.fmt)
					elif layer.color is not None:
						self.axes.errorbar(
								x=layer.x,
								y=layer.y,
								xerr=layer.xerrors,
								yerr=layer.yerrors,
								fmt=layer.fmt,
								color=layer.color)
				elif isinstance(layer,layers.Layer3D):
					self.axes.pcolor(
							layer.X,
							layer.Y,
							layer.C,
							alpha=layer.alpha,
							shading=layer.shading,
							cmap=layer.cm)
				layer.not_changed()
				self.drawn_layers.append(layer)

	def render_to_image(self,shape):
		self.render()

		dpi=self.figure.dpi
		self.figure.set_size_inches(float(shape[0])/dpi,float(shape[1])/dpi)

		agg_figure_container=mpl_backend_agg.FigureCanvasAgg(self.figure)
		agg_figure_container.draw()
		image_string=agg_figure_container.tostring_rgb()

		image=Image.fromstring("RGB",shape,image_string)
		return image
	
	def render_to_ps(self,shape,outfile):
		self.render()

		self.figure.set_size_inches(shape[0],shape[1])

		ps_figure_container=mpl_backend_ps.FigureCanvasPS(self.figure)
		ps_figure_container.print_eps(
				outfile=outfile,
				dpi=self.figure.dpi)
