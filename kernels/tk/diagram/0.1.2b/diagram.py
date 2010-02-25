# Maintainer: Friedrich Romstedt <friedrichromstedt@gmail.com>
# Copyright 2008 Friedrich Romstedt
#    This file is part of Diagram_cl.
#
#    Diagram_cl is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Diagram_cl is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Diagram_cl.  If not, see <http://www.gnu.org/licenses/>.
# $Last changed: 2008 Oct 16$
# Developed since: Aug 2008
# File version: 0.1.2b

import diagram_cl.panels.tk.diagram as tk_diagram

class Diagram:
	def __init__(self,master,diagram):
		self.diagram=diagram
		self.panel=tk_diagram.Diagram(
				master=master,
				event_handler_start_zoom=self.start_zoom,
				event_handler_zoom=self.zoom,
				event_handler_start_pan=self.start_pan,
				event_handler_pan=self.pan,
				event_handler_doubleclick=self.autozoom,
				image_computer=self.diagram.render_to_image)

	def update(self):
		self.panel.update()

	def map_to_axes_coords(self,disp_coords):
		bbox=self.diagram.axes.get_position()
		axes_position=(bbox.x0,bbox.y0,bbox.size[0],bbox.size[1]) # (l,b,w,h)
		return ((disp_coords[0]-axes_position[0])/axes_position[2],
				(disp_coords[1]-axes_position[1])/axes_position[3])
	
	def map_to_data_coords(self,axes_coords):
		lims=[self.diagram.axes.get_xlim(),self.diagram.axes.get_ylim()]
		return (lims[0][0]+(lims[0][1]-lims[0][0])*axes_coords[0],
				lims[1][0]+(lims[1][1]-lims[1][0])*axes_coords[1])

	def start_zoom(self,disp_coords):
		lims=[self.diagram.axes.get_xlim(),self.diagram.axes.get_ylim()]
		bbox=self.diagram.axes.get_position()
		axes_position=(bbox.x0,bbox.y0,bbox.size[0],bbox.size[1]) # (l,b,w,h)
		axes_coords=self.map_to_axes_coords(disp_coords)
		self.zoom_start_position=self.map_to_data_coords(axes_coords)
		self.zoom_original_distances=(
				[lims[0][0]-self.zoom_start_position[0],
				 lims[0][1]-self.zoom_start_position[0]],
				[lims[1][0]-self.zoom_start_position[1],
				 lims[1][1]-self.zoom_start_position[1]])

	def zoom(self,(zoomx,zoomy)):
		zoom_new_distances=(
				[self.zoom_original_distances[0][0]*zoomx,self.zoom_original_distances[0][1]*zoomx],
				[self.zoom_original_distances[1][0]*zoomy,self.zoom_original_distances[1][1]*zoomy])
		zoom_new_lims=(
				[self.zoom_start_position[0]+zoom_new_distances[0][0],
				 self.zoom_start_position[0]+zoom_new_distances[0][1]],
				[self.zoom_start_position[1]+zoom_new_distances[1][0],
				 self.zoom_start_position[1]+zoom_new_distances[1][1]])
		self.diagram.set_xlim(zoom_new_lims[0])
		self.diagram.set_ylim(zoom_new_lims[1])

	def start_pan(self):
		lims=[list(self.diagram.axes.get_xlim()),list(self.diagram.axes.get_ylim())]
		self.pan_start_lims=lims
		bbox=self.diagram.axes.get_position()
		axes_position=(bbox.x0,bbox.y0,bbox.size[0],bbox.size[1]) # (l,b,w,h)
		self.pan_ratio=(
				(lims[0][1]-lims[0][0])/axes_position[2],
				(lims[1][1]-lims[1][0])/axes_position[3])

	def pan(self,compensate):
		movement=(
				self.pan_ratio[0]*compensate[0],
				self.pan_ratio[1]*compensate[1])
		pan_new_lims=(
				[self.pan_start_lims[0][0]-movement[0],
				 self.pan_start_lims[0][1]-movement[0]],
				[self.pan_start_lims[1][0]-movement[1],
				 self.pan_start_lims[1][1]-movement[1]])
		self.diagram.set_xlim(pan_new_lims[0])
		self.diagram.set_ylim(pan_new_lims[1])

	def autozoom(self):
		self.diagram.set_autoscale_on(True)
