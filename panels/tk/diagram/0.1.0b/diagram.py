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
# $Last changed: 2008 Aug 22$
# Developed since: Aug 2008
# File version: 0.1.0b

import Tkinter
import ImageTk

class Diagram:
	def __init__(self,master,event_handler_start_zoom,event_handler_zoom,event_handler_start_pan,event_handler_pan,event_handler_doubleclick,image_computer):
		self.event_handler_start_zoom=event_handler_start_zoom
		self.event_handler_zoom=event_handler_zoom
		self.event_handler_start_pan=event_handler_start_pan
		self.event_handler_pan=event_handler_pan
		self.event_handler_doubleclick=event_handler_doubleclick
		self.image_computer=image_computer

		self.viewport,self.viewport_tag=None,None

		#master.pack_propagate(0)
		self.canvas=Tkinter.Canvas(master,highlightthickness=0,background='white')

		self.canvas.pack(expand=True,fill=Tkinter.BOTH)
		self.canvas.bind('<Configure>',self.tk_configure)
		self.canvas.bind('<ButtonPress-1>',self.tk_press_left_button)
		self.canvas.bind('<ButtonPress-3>',self.tk_press_right_button)
		self.canvas.bind('<ButtonRelease-1>',self.tk_release_left_button)
		self.canvas.bind('<ButtonRelease-3>',self.tk_release_right_button)
		self.canvas.bind('<Motion>',self.tk_motion)
		self.canvas.bind('<Double-Button-1>',self.double_left_button)
		self.pixelsize=None

		self.motion_origin=None
		self.zooming_origin=None
		self.zooming_initial_distances=None
		self.pan_cursor=None
		self.motion_mode='none'

	def map_to_display(self,(scrx,scry)):
		return (float(scrx)/self.pixelsize[0],1-float(scry)/self.pixelsize[1])

	def tk_configure(self,event):
		self.pixelsize=event.width,event.height
		self.update()

	def tk_press_left_button(self,event):
		disp_coords=self.map_to_display((event.x,event.y))
		self.motion_origin=(event.x,event.y)
		self.motion_mode='zoom'
		self.zooming_origin=disp_coords
		self.event_handler_start_zoom(disp_coords)

	def tk_press_right_button(self,event):
		disp_coords=self.map_to_display((event.x,event.y))
		self.pan_origin=disp_coords
		self.motion_mode='pan'
		self.event_handler_start_pan()

	def tk_release_left_button(self,event):
		self.motion_mode='none'

	def tk_release_right_button(self,event):
		self.motion_mode='none'

	def double_left_button(self,event):
		self.event_handler_doubleclick()
		self.update()

	def tk_motion(self,event):
		if self.motion_mode=='zoom':
			pixel_distances=(self.motion_origin[0]-event.x,event.y-self.motion_origin[1])
			factors=[(2.0**(pixel_distances[i]*0.02)) for i in (0,1)]
			self.event_handler_zoom(factors)
			self.update()
		elif self.motion_mode=='pan':
			disp_coords=self.map_to_display((event.x,event.y))
			compensate=[disp_coords[i]-self.pan_origin[i] for i in (0,1)]
			self.event_handler_pan(compensate)
			self.update()

	def update(self):
		if self.pixelsize is None: return
		image=self.image_computer(self.pixelsize)
		if self.viewport is not None and self.viewport_tag is not None:
			self.canvas.delete(self.viewport_tag)
		self.viewport=ImageTk.PhotoImage(image)
		self.viewport_tag=self.canvas.create_image((0,0),image=self.viewport,anchor='nw')
		self.canvas.update()
	
	def destroy(self):
		if self.viewport is not None and self.viewport_tag is not None:
			self.canvas.delete(self.viewport_tag)
		del self.viewport,self.viewport_tag
		self.canvas.destroy()
		del self.canvas
