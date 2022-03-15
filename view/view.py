from PyQt5.QtWidgets import *
# from pyqtgraph import PlotWidet, plot
# import pyqtgraph as pg
import pyqtgraph as pg
from QLed import QLed
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from time import sleep
import pathlib

class View(QApplication):
	def __init__(self, *args):
		super(View, self).__init__([])

		# ############# ROOT / FRAMES / WIDGETS #############
		self.root = None
		self.frames = {}
		self.widgets = {}
		self.config = {}

		self.power_line = None
		self.bat_soc_line = None
		self.bat_voltage_line = None
		self.bat_current_line = None

		self.create_config(args)

		self.select_colors()

		self.create_front()

		self.initialize()

		self.get_resolution()

	def create_config(self, *args):
		self.config = {
			'MVC': {},
			'scale': {},
			'init': {},
			'colors': {},
			'window': {},
			'layouts': {},
			'root': {},
			'frames': {},
			'widgets': {},
			'comms': {},
		}

		# MVC REF
		if True:
			self.config['MVC']['components'] = ['model', 'view', 'controller']
			self.config['MVC']['model'] = None
			self.config['MVC']['view'] = None
			self.config['MVC']['controller'] = None	
		
		# SCALE
		if True:
			self.config['scale']['abs'] = 1
			self.config['scale']['x']   = 1
			self.config['scale']['y']   = 1

		# INIT
		if True:
			self.config['init']['ip'] = '192.168.1.243'
			self.config['init']['port'] = 502
			self.config['init']['uid'] = 3
			self.config['init']['initialized'] = False

		# COLORS
		if True:
			self.config['colors']['black'] = '#000000'
			self.config['colors']['white'] = '#ffffff'
			self.config['colors']['red'] = '#660000'
			self.config['colors']['red_background'] = '#ff9999'
			self.config['colors']['red_background_2'] = '#ff6666'
			self.config['colors']['green'] = '#006600'
			self.config['colors']['green_background'] = '#99ff99'
			self.config['colors']['green_background_2'] = '#b2ff66'
			self.config['colors']['blue'] = '#0000cc'
			self.config['colors']['blue_background'] = '#9999ff'
			self.config['colors']['blue_background_2'] = '#6666ff'
			self.config['colors']['orange'] = '#ff8000'
			self.config['colors']['orange_background'] = '#ffcc99'
			self.config['colors']['grey'] = '#808080'
			self.config['colors']['grey_background'] = '#e0e0e0'
			self.config['colors']['grey_background_2'] = '#c0c0c0'
			self.config['colors']['yellow'] = '#ffff00'
			self.config['colors']['yellow_background'] = '#ffff99'

		# WINDOW
		if True:
			self.config['window']['base_width'] = 2560
			self.config['window']['base_height'] = 1080

			self.config['window']['name'] = None
			self.config['window']['width'] = None
			self.config['window']['height'] = None

		# LAYOUTS
		if True:
			self.config['layouts']['frame_spacing_x']     = 10
			self.config['layouts']['frame_spacing_y']     = 10
			self.config['layouts']['frame_margin_left']   = 4
			self.config['layouts']['frame_margin_top']    = 4
			self.config['layouts']['frame_margin_right']  = 4
			self.config['layouts']['frame_margin_bottom'] = 4

			self.config['layouts']['widget_spacing_x']     = 10
			self.config['layouts']['widget_spacing_y']     = 10
			self.config['layouts']['widget_margin_left']   = 4
			self.config['layouts']['widget_margin_top']    = 4
			self.config['layouts']['widget_margin_right']  = 4
			self.config['layouts']['widget_margin_bottom'] = 4		

			self.config['layouts']['default_spacing_x'] = 5
			self.config['layouts']['default_spacing_y'] = 5
		
		# ROOT
		if True:
			self.config['root']['title'] = 'SCADA'
			self.config['root']['width'] = 2000
			self.config['root']['height'] = 1000
		
		# WIDGETS
		if True:
			self.config['widgets']['borderstyle_none'] = "'none'"

			self.config['widgets']['fontsize_normal'] = 10
			self.config['widgets']['fontsize_small'] = 8
			self.config['widgets']['fontsize_big'] = 12

			self.config['widgets']['fontweight_normal'] = 'normal'			
			self.config['widgets']['fontweight_bold'] = 'bold'				

			self.config['widgets']['pad_x_1'] = 5
			self.config['widgets']['pad_y_1'] = 5

			self.config['widgets']['width_label'] = 125
			self.config['widgets']['height_label'] = 25

			self.config['widgets']['width_edit'] = 200
			self.config['widgets']['height_edit'] = 25

			self.config['widgets']['width_combo'] = 125
			self.config['widgets']['height_combo'] = 25
			
			self.config['widgets']['width_button'] = 160
			self.config['widgets']['height_button'] = 50
			self.config['widgets']['fontsize_button'] = 20
			self.config['widgets']['border_radius_button'] = 10

			self.config['widgets']['width_led'] = 50
			self.config['widgets']['height_led'] = 50

			self.config['widgets']['width_small_led'] = 20
			self.config['widgets']['height_small_led'] = 20
			self.config['widgets']['delta_x_small_led'] = 0
			self.config['widgets']['delta_y_small_led'] = 2

			self.config['widgets']['width_image'] = 50
			self.config['widgets']['height_image'] = 50

			self.config['widgets']['width_separator'] = 50
			self.config['widgets']['width_separator_edit'] = 125
			self.config['widgets']['height_separator'] = 25

			self.config['widgets']['width_message'] = 300
			self.config['widgets']['height_message'] = 25

			self.config['widgets']['width_graph'] = 500
			self.config['widgets']['height_graph'] = 300

		# FRAMES
		if True:
			# Frames -> Main
			if True:
				self.frames['main'] = None
				self.frames['control'] = None
				self.frames['graph'] = None

			# Frames -> Default
			if True:
				self.config['frames']['default'] = {}

				self.config['frames']['default']['pad_x_1'] = 10
				self.config['frames']['default']['pad_y_1'] = 10
				self.config['frames']['default']['pad_x_2'] = 2
				self.config['frames']['default']['pad_y_2'] = 2				

				self.config['frames']['default']['width'] = self.config['root']['width']
				self.config['frames']['default']['height'] = self.config['root']['height']
				self.config['frames']['default']['width_1'] = int(self.config['root']['width']/2.0)
				self.config['frames']['default']['height_1'] = int(self.config['root']['height'] - 2*self.config['frames']['default']['pad_y_1'])
				self.config['frames']['default']['width_2'] = int(self.config['frames']['default']['width_1']/2.0)
				self.config['frames']['default']['height_2'] = 20

				self.config['frames']['default']['init_x'] = 0
				self.config['frames']['default']['init_y'] = 0		
				self.config['frames']['default']['spacing_x'] = 5
				self.config['frames']['default']['spacing_y'] = 5
				self.config['frames']['default']['border-width'] = 1
				self.config['frames']['default']['border-style'] = 'solid'
				self.config['frames']['default']['border-radius'] = 4
				self.config['frames']['default']['color'] = self.config['colors']['grey_background']

			# Frames -> Logo
			if True:
				name = 'logo'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['width'] = 100
				self.config['frames'][name]['height'] = 50
				self.config['frames'][name]['init_x'] = 0
				self.config['frames'][name]['init_y'] = 0
				self.config['frames'][name]['spacing_x'] = 0
				self.config['frames'][name]['spacing_y'] = 0
				self.config['frames'][name]['color'] = self.config['colors']['red']

			# Frames -> Message
			if True:
				name = 'message'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames'][name]['height'] = 3 * self.config['widgets']['height_label']
				self.config['frames'][name]['init_x'] = 0
				self.config['frames'][name]['init_y'] = 0	
				self.config['frames'][name]['spacing_x'] = 0
				self.config['frames'][name]['spacing_y'] = 0				

				name = 'message-L'
				self.frames[name] = None
				self.config['frames'][name] = {}
				# self.config['frames'][name]['width'] = self.config['frames']['default']['width_2']
				# self.config['frames'][name]['height'] = 3 * self.config['widgets']['height_label']
				self.config['frames'][name]['width'] = 0.75 * self.config['frames']['message']['width']
				self.config['frames'][name]['height'] = self.config['frames']['message']['height']
				self.config['frames'][name]['init_x'] = 10
				self.config['frames'][name]['init_y'] = 10
				self.config['frames'][name]['spacing_x'] = 8
				self.config['frames'][name]['spacing_y'] = 8

				name = 'message-R'
				self.frames[name] = None
				self.config['frames'][name] = {}
				# self.config['frames'][name]['width'] = self.config['frames']['default']['width_2']
				# self.config['frames'][name]['height'] = 3 * self.config['widgets']['height_label']
				self.config['frames'][name]['width'] = 0.25 * self.config['frames']['message']['width']
				self.config['frames'][name]['height'] = self.config['frames']['message']['height']				
				self.config['frames'][name]['init_x'] = 10
				self.config['frames'][name]['init_y'] = 10
				self.config['frames'][name]['spacing_x'] = 8
				self.config['frames'][name]['spacing_y'] = 8

			# Frames -> Connection
			if True:
				self.frames['connection'] = None
				self.config['frames']['connection'] = {}		
				self.config['frames']['connection']['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames']['connection']['height'] = 6 * (self.config['widgets']['height_label'])

				self.frames['connection-L'] = None
				self.config['frames']['connection-L'] = {}
				self.config['frames']['connection-L']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['connection-L']['height'] = 5 * self.config['widgets']['height_label']
				self.config['frames']['connection-L']['init_x'] = 10
				self.config['frames']['connection-L']['init_y'] = 10
				self.config['frames']['connection-L']['spacing_x'] = 8
				self.config['frames']['connection-L']['spacing_y'] = 8

				self.frames['connection-R'] = None
				self.config['frames']['connection-R'] = {}		
				self.config['frames']['connection-R']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['connection-R']['height'] = 5 * self.config['widgets']['height_label']
				self.config['frames']['connection-R']['init_x'] = 10
				self.config['frames']['connection-R']['init_y'] = 10
				self.config['frames']['connection-R']['spacing_x'] = 8		
				self.config['frames']['connection-R']['spacing_y'] = 8		

			# Frames -> Control
			if True:
				self.frames['control'] = None
				self.config['frames']['control'] = {}		
				self.config['frames']['control']['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames']['control']['height'] = 3 * self.config['widgets']['height_label']	+ 2*self.config['frames']['default']['spacing_y']
				self.config['frames']['control']['init_x'] = 10
				self.config['frames']['control']['init_y'] = 20
				self.config['frames']['control']['spacing_x'] = 8
				self.config['frames']['control']['spacing_y'] = 8	

			# Frames -> Info
			if True:
				self.frames['info'] = None
				self.config['frames']['info'] = {}		
				self.config['frames']['info']['width'] = self.config['frames']['default']['width_1']
				self.config['frames']['info']['height'] = 5 * self.config['widgets']['height_label']
				self.config['frames']['info']['width_widget'] = 400
				self.config['frames']['info']['init_x'] = 10
				self.config['frames']['info']['init_y'] = 15
				self.config['frames']['info']['spacing_x'] = 8
				self.config['frames']['info']['spacing_y'] = 8				
				
			# Frames -> Read inverter
			if True:
				self.frames['read_inverter'] = None
				self.config['frames']['read_inverter'] = {}		
				self.config['frames']['read_inverter']['ref'] = None		
				self.config['frames']['read_inverter']['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames']['read_inverter']['height'] = 6 * self.config['widgets']['height_label']			

				self.frames['read_inverter-L'] = None
				self.config['frames']['read_inverter-L'] = {}
				self.config['frames']['read_inverter-L']['ref'] = None
				self.config['frames']['read_inverter-L']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['read_inverter-L']['height'] = 70
				self.config['frames']['read_inverter-L']['init_x'] = 10
				self.config['frames']['read_inverter-L']['init_y'] = 10
				self.config['frames']['read_inverter-L']['spacing_y'] = 8

				self.frames['read_inverter-R'] = None
				self.config['frames']['read_inverter-R'] = {}
				self.config['frames']['read_inverter-R']['ref'] = None
				self.config['frames']['read_inverter-R']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['read_inverter-R']['height'] = 70
				self.config['frames']['read_inverter-R']['init_x'] = 10
				self.config['frames']['read_inverter-R']['init_y'] = 10
				self.config['frames']['read_inverter-R']['spacing_y'] = 8	

			# Frames -> Read battery
			if True:
				self.frames['read_battery'] = None
				self.config['frames']['read_battery'] = {}
				self.config['frames']['read_battery']['ref'] = None		
				self.config['frames']['read_battery']['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames']['read_battery']['height'] = 6 * self.config['widgets']['height_label']	

				self.frames['read_battery-L'] = None
				self.config['frames']['read_battery-L'] = {}
				self.config['frames']['read_battery-L']['ref'] = None
				self.config['frames']['read_battery-L']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['read_battery-L']['height'] = 70
				self.config['frames']['read_battery-L']['init_x'] = 10
				self.config['frames']['read_battery-L']['init_y'] = 10
				self.config['frames']['read_battery-L']['spacing_y'] = 8	

				self.frames['read_battery-R'] = None
				self.config['frames']['read_battery-R'] = {}
				self.config['frames']['read_battery-R']['ref'] = None
				self.config['frames']['read_battery-R']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['read_battery-R']['height'] = 70
				self.config['frames']['read_battery-R']['init_x'] = 10
				self.config['frames']['read_battery-R']['init_y'] = 10
				self.config['frames']['read_battery-R']['spacing_y'] = 8	

			# Frames -> Write
			if True:
				self.frames['write'] = None
				self.config['frames']['write'] = {}
				self.config['frames']['write']['ref'] = None		
				self.config['frames']['write']['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames']['write']['height'] = 3 * self.config['widgets']['height_label'] + 2*self.config['frames']['default']['spacing_y']

				self.frames['write-L'] = None
				self.config['frames']['write-L'] = {}
				self.config['frames']['write-L']['ref'] = None
				self.config['frames']['write-L']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['write-L']['height'] = 70
				self.config['frames']['write-L']['init_x'] = 10
				self.config['frames']['write-L']['init_y'] = 10
				self.config['frames']['write-L']['spacing_y'] = 8	

				self.frames['write-R'] = None
				self.config['frames']['write-R'] = {}
				self.config['frames']['write-R']['ref'] = None
				self.config['frames']['write-R']['width'] = self.config['frames']['default']['width_2']
				self.config['frames']['write-R']['height'] = 70
				self.config['frames']['write-R']['init_x'] = 10
				self.config['frames']['write-R']['init_y'] = 10
				self.config['frames']['write-R']['spacing_y'] = 8	

			# Frames -> Test		
			if True:
				name = 'test'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['ref'] = None		
				self.config['frames'][name]['width'] = self.config['frames']['default']['width_1'] - self.config['frames']['default']['spacing_x']
				self.config['frames'][name]['height'] = 4 * self.config['widgets']['height_label'] + 2*self.config['frames']['default']['spacing_y']

				name = 'test-L'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['ref'] = None
				self.config['frames'][name]['width'] = self.config['frames']['default']['width_2']
				self.config['frames'][name]['height'] = 70
				self.config['frames'][name]['init_x'] = 10
				self.config['frames'][name]['init_y'] = 10
				self.config['frames'][name]['spacing_y'] = 8	

				name = 'test-R'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['ref'] = None
				self.config['frames'][name]['width'] = self.config['frames']['default']['width_2']
				self.config['frames'][name]['height'] = 70
				self.config['frames'][name]['init_x'] = 10
				self.config['frames'][name]['init_y'] = 10
				self.config['frames'][name]['spacing_y'] = 8	

			# Frames -> Graph logo
			if True:
				name = 'graph_logo'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['width'] = 800
				self.config['frames'][name]['height'] = 50
				self.config['frames'][name]['init_x'] = 0
				self.config['frames'][name]['init_y'] = 0
				self.config['frames'][name]['spacing_x'] = 0
				self.config['frames'][name]['spacing_y'] = 0
				self.config['frames'][name]['color'] = self.config['colors']['red']

			# Frames -> Graphs
			if True:
				name = 'graphs'
				self.frames[name] = None
				self.config['frames'][name] = {}
				self.config['frames'][name]['width'] = 1200
				self.config['frames'][name]['height'] = 775
				self.config['frames'][name]['init_x'] = 20
				self.config['frames'][name]['init_y'] = 95
				self.config['frames'][name]['spacing_x'] = 20
				self.config['frames'][name]['spacing_y'] = 20
				self.config['frames'][name]['color'] = self.config['colors']['blue']

		# VALUES
		if True:
			self.values = {
				'window': {},
				'test': {},
				'comms_inverter': {},
				'comms_battery': {},
				'inverter': {},
				'battery': {},
			}

			# VALUES - main
			self.values['window']['message']            = None
			self.values['window']['message_alt']        = None
			self.values['window']['running_order']      = None
			self.values['window']['setpoint_val']       = None
			self.values['window']['setpoint_dir']       = None
			self.values['window']['setpoint_type']      = None
			self.values['window']['setpoint_indicator'] = None
			
			# VALUES - test
			self.values['test']['path'] = None
			self.values['test']['ok'] = None
			self.values['test']['running'] = None
			self.values['test']['finished'] = None
			self.values['test']['total_time'] = None
			self.values['test']['total_it'] = None
			self.values['test']['it'] = None
					
			# VALUES - comms inverter
			self.values['comms_inverter']['manufacturer'] = None
			self.values['comms_inverter']['connected']    = None
			self.values['comms_inverter']['autocomm']     = None
			self.values['comms_inverter']['ip']           = None
			self.values['comms_inverter']['port']         = None
			self.values['comms_inverter']['uid']          = None

			# VALUES - comms battery
			self.values['comms_battery']['manufacturer'] = None
			self.values['comms_battery']['connected']    = None
			self.values['comms_battery']['autocomm']     = None
			self.values['comms_battery']['ip']           = None
			self.values['comms_battery']['port']         = None
			self.values['comms_battery']['uid']          = None

			# VALUES - inverter
			self.values['inverter']['manufacturer'] = None
			self.values['inverter']['model']        = None	
			self.values['inverter']['serial']       = None

			self.values['inverter']['status']    = None
			self.values['inverter']['running']   = None
			self.values['inverter']['operation'] = None

			self.values['inverter']['power_3'] = None
			self.values['inverter']['power_r'] = None
			self.values['inverter']['power_s'] = None
			self.values['inverter']['power_t'] = None

			self.values['inverter']['bat_status']  = None
			self.values['inverter']['bat_voltage'] = None
			self.values['inverter']['bat_current'] = None
			self.values['inverter']['bat_soc']     = None

			# VALUES - battery
			self.values['battery']['manufacturer'] = None
			self.values['battery']['model']        = None	
			self.values['battery']['serial']       = None

			self.values['battery']['status']       = None
			self.values['battery']['running']      = None

			self.values['battery']['voltage']      = None
			self.values['battery']['current']      = None
			self.values['battery']['soc']          = None
			self.values['battery']['ch_current']   = None
			self.values['battery']['dsch_current'] = None
			self.values['battery']['ch_voltage']   = None
			self.values['battery']['dsch_voltage'] = None

		# COMMS
		if True:
			self.config['comms'] = {
				'inverter': {},
				'battery': {},
				'default': {
					'ip': None,
					'port': None,
					'uid': None
				},
			}

	def get_resolution(self):
		screen = self.primaryScreen()
		size = screen.size()
		
		self.config['window']['name'] = screen.name()
		self.config['window']['width'] = size.width()
		self.config['window']['height'] = size.height()

		# print(f"Screen: {self.config['window']['name']}")
		# print(f"Screen size: {self.config['window']['width']} x {self.config['window']['height']}")

		# for index, screen_no in enumerate(self.screens()):
		# 	size = screen_no.size()
		# 	print(f"Screen {index} -> {size}")

		# for displayNr in range(QtWidgets.QDesktopWidget().screenCount()):
		# 	sizeObject = QtWidgets.QDesktopWidget().screenGeometry(displayNr)
		# 	print("Display: " + str(displayNr) + " Screen size : " + str(sizeObject.width()) + "x" + str(sizeObject.height()))		

	def set_mvc_refs(self, data, verbose = False):
		for mvc in data:
			if mvc in self.config['MVC']['components']:
				if mvc == 'view':
					self.config['MVC'][mvc] = self
				else:
					self.config['MVC'][mvc] = data[mvc]

		if verbose:
			print("\nView MVC refs changed!")
			print(f"  - Model: 		{self.config['MVC']['model']}")
			print(f"  - View: 		{self.config['MVC']['view']}")
			print(f"  - Controller: {self.config['MVC']['controller']}")

	def set_scale(self, data):
		try:
			self.config['scale']['abs'] = data['abs']
		except:
			self.config['scale']['abs'] = 1

		self.config['scale']['x'] = self.config['scale']['abs']
		self.config['scale']['y'] = self.config['scale']['abs']

		self.apply_scale_all()
		self.recreate_front()

	def show_scale(self):
		print("\nView scale:")
		print(f"  - Abs: {self.config['scale']['abs']}")
		print(f"  - x: {self.config['scale']['x']}")
		print(f"  - y: {self.config['scale']['y']}")

	def apply_scale(self, data, mod = 1):
			for key in data:
				if ('_x' in key) or ('_left' in key) or ('_right' in key) or ('width' in key):
					data[key] = max([int(data[key] * self.config['scale']['x']) * mod, 1])
				elif ('_y' in key) or ('_top' in key) or ('_bottom' in key) or ('height' in key):
					data[key] = max([int(data[key] * self.config['scale']['y']) * mod, 1])
				elif ('fontsize' in key):
					data[key] = max([int(data[key] * self.config['scale']['abs']) * mod, 1])

			return data
		
	def apply_scale_all(self):

		# Apply scale to self.config['root']
		self.config['root'] = self.apply_scale(self.config['root'])		

		# Apply scale to self.config['layouts']
		self.config['layouts'] = self.apply_scale(self.config['layouts'])

		# Apply scale to self.config['widget']
		self.config['widgets'] = self.apply_scale(self.config['widgets'])

		# Apply scale to each element in self.config['frames']
		for frame in self.config['frames']:
			self.config['frames'][frame] = self.apply_scale(self.config['frames'][frame])

	def set_comms(self):
		# Comms inverter
		self.values['comms_inverter']['manufacturer']  = str(self.widgets['manufacturer_inv'].currentText())
		self.values['comms_inverter']['ip']         = self.widgets['ip_inv'].text()
		self.values['comms_inverter']['port']       = self.widgets['port_inv'].text()
		self.values['comms_inverter']['uid']        = self.widgets['uid_inv'].text()

		# Comms battery
		self.values['comms_battery']['manufacturer']  = str(self.widgets['manufacturer_bat'].currentText())
		self.values['comms_battery']['ip']         = self.widgets['ip_bat'].text()
		self.values['comms_battery']['port']       = self.widgets['port_bat'].text()
		self.values['comms_battery']['uid']        = self.widgets['uid_bat'].text()

		data = {
			'inverter': self.values['comms_inverter'],
			'battery': self.values['comms_battery']
		}

		self.config['MVC']['controller'].set_comms(data)

	def show_comms(self):
		print("\nView inverter comms:")
		self.show_dict(self.values['comms_inverter'])

		print("\nView battery comms:")
		self.show_dict(self.values['comms_battery'])

	def show_dict(self, dict):
		try:
			for key, value in dict.items():
				print(f"{key} -> {value}")
		except:
			return None

	def select_colors(self):
		self.selected_colors = {}

		self.selected_colors['main_background'] = self.config['colors']['grey_background']

		self.selected_colors['background_1'] = self.config['colors']['grey_background']
		self.selected_colors['background_2'] = self.config['colors']['grey_background_2']
		
		self.selected_colors['button'] = self.config['colors']['grey']

		self.selected_colors['exit_button'] = self.config['colors']['red']

	def create_root(self):
		self.root = QMainWindow()

		self.root.setWindowTitle(self.config['root']['title'])
		self.root.setFixedSize(self.config['root']['width'], self.config['root']['height'])
		self.root.setStyleSheet(f"background-color: {self.config['colors']['grey_background']}")
			
	def create_frames(self):
		# MAIN FRAME
		frame_main = QFrame(self.root)
		frame_main.setStyleSheet(f"background-color: {self.selected_colors['main_background']}")
		self.frames['main'] = frame_main
		self.root.setCentralWidget(self.frames['main'])

		# Creamos los frames MAIN
		main_json = {
			'base_frame': 'main',
			'layout': True,
			'list': [
				{
					'name': 'control',
					'type': 'frame',
					# 'background-color': self.selected_colors['main_background'],
					'background-color': self.config['colors']['white'],
					'border_width': 2, 
					'border_radius': 10, 
					'border-style': 'solid',
					'width': self.config['frames']['default']['width_1'],
					'height': self.config['frames']['default']['height_1'],
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'graph',
					'type': 'frame',
					# 'background-color': self.selected_colors['main_background'],
					'background-color': self.config['colors']['red'],
					'border_width': 2, 
					'border_radius': 10, 
					'border-style': 'solid',
					'width': self.config['frames']['default']['width_1'],
					'height': self.config['frames']['default']['height_1'],
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = main_json)



		### 1. Creamos los frames CONTROL
		control_json = {
			'base_frame': 'control',
			'layout': False,
			'list': [
				{
					'name': 'logo',
					'type': 'frame',
					'background-color': self.config['frames']['logo']['color'],
				}, 				
				{
					'name': 'message',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],
				}, 
				{
					'name': 'connection',
					'type': 'frame',
					'background-color': self.selected_colors['background_2'],
				}, 		
				{
					'name': 'control',
					'type': 'frame',
					'background-color': self.selected_colors['background_2'],
				}, 		
				{
					'name': 'info',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],
				}, 		
				{
					'name': 'read_inverter',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],
				}, 	 	
				{
					'name': 'read_battery',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],		
				},
				{
					'name': 'write',
					'type': 'frame',
					'background-color': self.selected_colors['background_2'],
				}, 
				{
					'name': 'test',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],
				}, 
			]										
		}
		control_json = self.f_create_layout(control_json, type = 'vertical', init_x = 0, init_y = 0, spacing_y = 0)
		self.f_create_widget(widgets_json = control_json)


		### 2. Creamos los frames GRAPH
		graph_json = {
			'base_frame': 'graph',
			'layout': False,
			'list': [
				{
					'name': 'graph_logo',
					'type': 'frame',
					'background-color': self.config['frames']['logo']['color'],
				}, 				
				{
					'name': 'graphs',
					'type': 'frame',
					'background-color': self.selected_colors['background_1'],
				}, 
			]										
		}
		graph_json = self.f_create_layout(graph_json, type = 'vertical', init_x = 0, init_y = 0, spacing_y = 0)
		self.f_create_widget(widgets_json = graph_json)



		### 1.1 Creamos los subframes MESSAGE
		message_json = {
			'base_frame': 'message',
			'layout': False,
			'list': [
				{
					'name': 'message-L',
					'type': 'frame',
					'border-style': 'none',
					'width': self.config['frames']['message-L']['width'],
					'height': self.config['frames']['message-L']['height'],
				}, 
				{
					'name': 'message-R',
					'type': 'frame',
					'border-style': 'none',
					'width': self.config['frames']['message-R']['width'],
					'height': self.config['frames']['message-R']['height'],
				}, 	
			]										
		}
		message_json = self.f_create_layout(message_json, type = 'horizontal', init_x = 0, init_y = 0, spacing_x = 0, spacing_y = 0)
		self.f_create_widget(widgets_json = message_json)
		
		### 1.2 Creamos los subframes CONNECTION
		connection_json = {
			'base_frame': 'connection',
			'layout': True,
			'list': [
				{
					'name': 'connection-L',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'connection-R',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = connection_json)

		### 1.3 Creamos los subfames INFO

		### 1.4 Creamos los subframes CONTROL

		### 1.5 Creamos los subframes READ_INVERTER
		read_inverter_json = {
			'base_frame': 'read_inverter',
			'layout': True,
			'list': [
				{
					'name': 'read_inverter-L',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'read_inverter-R',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = read_inverter_json)

		### 1.6 Creamos los subframes READ_BATTERY
		read_battery_json = {
			'base_frame': 'read_battery',
			'layout': True,
			'list': [
				{
					'name': 'read_battery-L',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'read_battery-R',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = read_battery_json)

		### 1.7 Creamos los subframes WRITE
		write_json = {
			'base_frame': 'write',
			'layout': True,
			'list': [
				{
					'name': 'write-L',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'write-R',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = write_json)

		### 1.8 Creamos los subframes TEST
		test_json = {
			'base_frame': 'test',
			'layout': True,
			'list': [
				{
					'name': 'test-L',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 0,
				}, 
				{
					'name': 'test-R',
					'type': 'frame',
					'border-style': 'none',
					'x': 0,
					'y': 1,
				}, 		
			]										
		}
		self.f_create_widget(widgets_json = test_json)		

	def create_widgets(self):
		# ############# LOGO #############
		logo_json = {
			'base_frame': 'logo',
			'layout': False,
			'list': [
				{
					'name': 'logo',
					'type': 'image',
					'image': 'Cegasa Negro-Verde.jpg',
					'save': True,
					'border-style': 'none',
				},
			]
		}
		logo_json = self.f_create_layout(logo_json, type = 'vertical')
		self.f_create_widget(logo_json)

		# ############# MESSAGE #############
		# Message Left
		message_L_json = {
			'base_frame': 'message-L',
			'layout': False,
			'list': [
				{
					'name': 'message',
					'type': 'label',
					'save': True,
					'text': 'Disconnected from server',
					'border-style': 'none',
					'width': self.config['widgets']['width_message'],
				},			
				# {
				# 	'name': 'tmp',
				# 	'type': 'button',
				# 	'save': False,
				# 	'function': self.plot_power_graph,
				# 	'text': 'Plot',
				# 	'background-color': self.selected_colors['button'],
				# 	'border-style': 'solid',
				# 	'border-width': 4,
				# },						
			]
		}
		message_L_json = self.f_create_layout(message_L_json, type = 'horizontal')
		self.f_create_widget(message_L_json)

		# Message Right
		message_R_json = {
			'base_frame': 'message-R',
			'layout': False,
			'list': [
				{
					'name': 'exit',
					'type': 'button',
					'save': True,
					'function': self.exit,
					'text': 'Exit',
					'background-color': self.selected_colors['exit_button'],
					'border-style': 'solid',
					'border-radius': self.config['widgets']['border_radius_button'],
				},			
			]
		}
		message_R_json = self.f_create_layout(message_R_json, type = 'vertical')
		self.f_create_widget(message_R_json)			

		# ############# CONNECTION #############
		# Connection Left
		connection_L_json = {
			'base_frame': 'connection-L',
			'layout': False,
			'list': [
				{
					'name': 'inverter_label',
					'type': 'label',
					'save': False,
					'text': 'INVERTER',
					'border-style': 'none',
					'font-weight': 'bold',
					'font-size': self.config['widgets']['fontsize_big'],
				},					
				{
					'name': 'manufacturer_inv',
					'type': 'combo',
					'elements': ['SMA', 'Victron', 'Ingeteam'],
					'save': True,
					'background-color': self.config['colors']['white'],
				},
				{
					'name': 'conn_state_inv',
					'type': 'led',
					'save': True,
					'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
					'shape': QLed.Circle, 		# Circle, Round, Square, Triangle
					'width': self.config['widgets']['width_small_led'],
					'height': self.config['widgets']['height_small_led'],
					'delta_y': self.config['widgets']['delta_y_small_led'],
				},							
				{
					'name': 'ip_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Ip',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'ip_inv',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},	
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},					
				{
					'name': 'port_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Port',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'port_inv',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},	
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},							
				{
					'name': 'uid_inv_label',
					'type': 'label',
					'save': False,
					'text': 'UID',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'uid_inv',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},																										
			]
		}
		connection_L_json = self.f_create_layout(connection_L_json, type = 'vertical', group = 3)
		self.f_create_widget(connection_L_json)

		# Connection Right
		connection_R_json = {
			'base_frame': 'connection-R',
			'list': [
				{
					'name': 'battery_label',
					'type': 'label',
					'save': False,
					'text': 'BATTERY',
					'border-style': 'none',
					'font-weight': 'bold',
					'font-size': self.config['widgets']['fontsize_big'],
				},						
				{
					'name': 'manufacturer_bat',
					'type': 'combo',
					'elements': ['Cegasa'],
					'save': True,
					'background-color': self.config['colors']['white'],
				},	
				{
					'name': 'conn_state_bat',
					'type': 'led',
					'save': True,
					'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
					'shape': QLed.Circle, 		# Circle, Round, Square, Triangle
					'width': self.config['widgets']['width_small_led'],
					'height': self.config['widgets']['height_small_led'],
					'delta_y': self.config['widgets']['delta_y_small_led'],
				},							
				{
					'name': 'ip_bat_label',
					'type': 'label',
					'save': False,
					'text': 'Ip',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'ip_bat',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},	
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},					
				{
					'name': 'port_bat_label',
					'type': 'label',
					'save': False,
					'text': 'Port',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'port_bat',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},	
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},								
				{
					'name': 'uid_bat_label',
					'type': 'label',
					'save': False,
					'text': 'UID',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'uid_bat',
					'type': 'edit',
					'save': True,
					'background-color': 'white',
				},	
				{
					'name': 'sep',
					'type': 'separator',
					'save': False,
					'width': 0
				},																
			]
		}
		connection_R_json = self.f_create_layout(connection_R_json, type = 'vertical', group = 3)
		self.f_create_widget(connection_R_json)

		# ############# CONTROL #############
		control_json = {
			'base_frame': 'control',
			'layout': False,
			'list': [
				{
					'name': 'separator',
					'type': 'separator',
					'save': False,
					'border-style': 'none',
				},					
				{
					'name': 'connect',
					'type': 'button',
					'save': True,
					'function': self.connect,
					'text': 'Connect',
					'background-color': self.selected_colors['button'],
					'border-style': 'solid',
					'border-width': 4,
				},					
				{
					'name': 'separator',
					'type': 'label',
					'save': False,
					'border-style': 'none',
				},				
				{
					'name': 'run_state_inv',
					'type': 'led',
					'save': True,
					'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
					'shape': QLed.Square, 		# Circle, Round, Square, Triangle
				},	
				{
					'name': 'run',
					'type': 'button',
					'save': True,
					'function': self.run,
					'text': 'Run',
					'background-color': self.selected_colors['button'],
					'border_syle': 'solid',
				},						
			]
		}
		control_json = self.f_create_layout(control_json, type = 'horizontal')
		self.f_create_widget(control_json)

		# ############# INFO #############
		info_json = {
			'base_frame': 'info',
			'layout': False,
			'list': [
				{
					'name': 'manufacturer_label',
					'type': 'label',
					'save': False,
					'text': 'Manufacturer',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'manufacturer',
					'type': 'edit',
					'save': True,
					'readonly': True,
					'width': self.config['frames']['info']['width_widget'],
				},	
				{
					'name': 'model_label',
					'type': 'label',
					'save': False,
					'text': 'Model',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'model',
					'type': 'edit',
					'save': True,
					'readonly': True,
					'width': self.config['frames']['info']['width_widget'],
				},				
				{
					'name': 'serial_label',
					'type': 'label',
					'save': False,
					'text': 'Serial',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'serial',
					'type': 'edit',
					'save': True,
					'readonly': True,
					'width': self.config['frames']['info']['width_widget'],
				},													
			]
		}
		info_json = self.f_create_layout(info_json, type = 'vertical', group = 2)
		self.f_create_widget(info_json)

		# ############# READ INVERTER #############
		# Read Inverter Left
		read_inv_L_json = {
			'base_frame': 'read_inverter-L',
			'list': [
				{
					'name': 'status_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Status',
					'border-style': self.config['widgets']['borderstyle_none'],
					'font-weight': 'bold',
				},
				{
					'name': 'status_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},	
				{
					'name': 'soc_inv_label',
					'type': 'label',
					'save': False,
					'text': 'SoC [%]',
					'border-style': self.config['widgets']['borderstyle_none'],
					'font-weight': 'bold',
				},
				{
					'name': 'soc_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},				
				{
					'name': 'voltage_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Voltage [V]',
					'border-style': self.config['widgets']['borderstyle_none'],
					'font-weight': 'bold',
				},
				{
					'name': 'voltage_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},		
				{
					'name': 'current_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Current [A]',
					'border-style': self.config['widgets']['borderstyle_none'],
					'font-weight': 'bold',
				},
				{
					'name': 'current_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},																
			]
		}
		read_inv_L_json = self.f_create_layout(read_inv_L_json, type = 'vertical', group = 2)
		self.f_create_widget(read_inv_L_json)	

		# Read Inverter Right
		read_inv_R_json = {
			'base_frame': 'read_inverter-R',
			'list': [
				{
					'name': 'power_3_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Power [W]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'power_3_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},	
				{
					'name': 'power_r_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Power R [W]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'power_r_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},				
				{
					'name': 'power_s_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Power S [W]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'power_s_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},		
				{
					'name': 'power_t_inv_label',
					'type': 'label',
					'save': False,
					'text': 'Power T [W]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'power_t_inv',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},																
			]
		}
		read_inv_R_json = self.f_create_layout(read_inv_R_json, type = 'vertical', group = 2)
		self.f_create_widget(read_inv_R_json)	

		# ############# READ BATTERY #############
		# Read Battery Left
		read_bat_L_json = {
			'base_frame': 'read_battery-L',
			'list': [
				{
					'name': 'status_bat_label',
					'type': 'label',
					'save': False,
					'text': 'Status',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'status_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},	
				{
					'name': 'soc_bat_label',
					'type': 'label',
					'save': False,
					'text': 'SoC [%]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'soc_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},				
				{
					'name': 'voltage_bat_label',
					'type': 'label',
					'save': False,
					'text': 'Voltage [V]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'voltage_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},		
				{
					'name': 'current_bat_label',
					'type': 'label',
					'save': False,
					'text': 'Current [A]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'current_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},																
			]
		}
		read_bat_L_json = self.f_create_layout(read_bat_L_json, type = 'vertical', group = 2)
		self.f_create_widget(read_bat_L_json)	

		# Read Battery Right
		read_bat_R_json = {
			'base_frame': 'read_battery-R',
			'list': [
				{
					'name': 'ch_current_label',
					'type': 'label',
					'save': False,
					'text': 'Charge curr [A]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'ch_current_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},	
				{
					'name': 'dsch_current_label',
					'type': 'label',
					'save': False,
					'text': 'Discharge curr [A]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'dsch_current_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},				
				{
					'name': 'ch_voltage_label',
					'type': 'label',
					'save': False,
					'text': 'Charge volt [V]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'ch_voltage_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},		
				{
					'name': 'dsch_voltage_label',
					'type': 'label',
					'save': False,
					'text': 'Discharge volt [V]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'dsch_voltage_bat',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},																
			]
		}
		read_bat_R_json = self.f_create_layout(read_bat_R_json, type = 'vertical', group = 2)
		self.f_create_widget(read_bat_R_json)	

		# ############# WRITE #############
		# Write Left
		write_L_json = {
			'base_frame': 'write-L',
			'layout': False,
			'list': [
				{
					'name': 'setpoint_label',
					'type': 'label',
					'save': False,
					'text': 'Setpoint [W]',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'setpoint_val',
					'type': 'edit',
					'save': True,
					'background-color': self.config['colors']['white'],
				},	
				{
					'name': 'update_setpoint',
					'type': 'button',
					'function': self.update_setpoint,
					'save': True,
					'border-style': 'none',
					'text': 'Update SP',
					'width': self.config['widgets']['width_label'],
					'height': self.config['widgets']['height_label'],
				},
				{
					'name': 'setpoint_dir',
					'type': 'combo',
					'elements': ['Rest', 'Charge', 'Discharge'],
					'save': True,
					'background-color': self.config['colors']['white'],
				},															
				# {
				# 	'name': 'test_label',
				# 	'type': 'label',
				# 	'save': False,
				# 	'text': '   TEST',
				# 	'border-style': 'none',
				# 	'font-weight': 'bold',
				# },
				# {
				# 	'name': 'test_path',
				# 	'type': 'edit',
				# 	'save': True,
				# 	'readonly': True,
				# 	'text': "Not loaded...",
				# 	'border-style': 'none',
				# 	'width': 600,
				# },
				# {
				# 	'name': 'test_loaded',
				# 	'type': 'led',
				# 	'save': True,
				# 	'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
				# 	'shape': QLed.Circle, 		# Circle, Round, Square, Triangle
				# },	
				# {
				# 	'name': 'test_load',
				# 	'type': 'button',
				# 	'save': True,
				# 	'function': self.load_test,
				# 	'text': 'Load',
				# 	'background-color': self.selected_colors['button'],
				# },
			]
		}
		write_L_json = self.f_create_layout(write_L_json, type = 'vertical', group = 2)
		self.f_create_widget(write_L_json)		

		# Write Right
		write_R_json = {
			'base_frame': 'write-R',
			'layout': False,
			'list': [
				{
					'name': 'setpoint_type',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},
				{
					'name': 'separator',
					'type': 'separator',
					'save': False,
					'border-style': 'none',
				},
				{
					'name': 'setpoint_indicator',
					'type': 'edit',
					'save': True,
					'readonly': True,
				},
				{
					'name': 'separator',
					'type': 'separator',
					'save': False,
					'border-style': 'none',
				},
				# {
				# 	'name': 'separator',
				# 	'type': 'separator',
				# 	'save': False,
				# 	'border-style': 'none',
				# },
				# {
				# 	'name': 'separator',
				# 	'type': 'separator',
				# 	'save': False,
				# 	'border-style': 'none',
				# },								
				# {
				# 	'name': 'test_running',
				# 	'type': 'led',
				# 	'save': True,
				# 	'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
				# 	'shape': QLed.Square, 		# Circle, Round, Square, Triangle
				# },	
				# {
				# 	'name': 'test_run',
				# 	'type': 'button',
				# 	'save': True,
				# 	'function': self.run_test,
				# 	'text': 'Run',
				# 	'background-color': self.selected_colors['button'],
				# },
			]
		}
		write_R_json = self.f_create_layout(write_R_json, type = 'vertical', group = 2)
		self.f_create_widget(write_R_json)			

		# ############# TEST #############
		# Test Left
		test_L_json= {
			'base_frame': 'test-L',
			'layout': False,
			'list': [														
				{
					'name': 'test_label',
					'type': 'label',
					'save': False,
					'text': '   TEST',
					'border-style': 'none',
					'font-weight': 'bold',
				},
				{
					'name': 'test_path',
					'type': 'edit',
					'save': True,
					'readonly': True,
					'text': "Not loaded...",
					'border-style': 'none',
					'width': 600,
				},
				{
					'name': 'test_ok',
					'type': 'led',
					'save': True,
					'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
					'shape': QLed.Circle, 		# Circle, Round, Square, Triangle
				},	
				{
					'name': 'test_check',
					'type': 'button',
					'save': True,
					'function': self.check_test,
					'text': 'Check',
					'background-color': self.selected_colors['button'],
				},
			]
		}			
		test_L_json = self.f_create_layout(test_L_json, type = 'vertical', group = 2)
		self.f_create_widget(test_L_json)

		# Test Right
		test_R_json = {
			'base_frame': 'test-R',
			'layout': False,
			'list': [
				{
					'name': 'test_time',
					'type': 'edit',
					'save': True,
					'read-only': True,
				},
				{
					'name': 'test_it',
					'type': 'edit',
					'save': True,
					'read-only': True,
				},								
				{
					'name': 'test_running',
					'type': 'led',
					'save': True,
					'on-color': QLed.Green, 	# Red, Green, Yellow, Grey, Orange, Purple, Blue
					'shape': QLed.Square, 		# Circle, Round, Square, Triangle
				},	
				{
					'name': 'test_run',
					'type': 'button',
					'save': True,
					'function': self.run_test,
					'text': 'Run',
					'background-color': self.selected_colors['button'],
				},
			]
		}
		test_R_json = self.f_create_layout(test_R_json, type = 'vertical', group = 2)
		self.f_create_widget(test_R_json)	

		# GRAPHS
		graphs_json = {
			'base_frame': 'graphs',
			'layout': False,
			'list': [
				{
					'name': 'graph_power',
					'type': 'graph',
					'save': True,
					'title': 'Inverter - Power'
				},
				{
					'name': 'graph_bat_soc',
					'type': 'graph',
					'save': True,
					'title': 'Inverter - Battery SoC'
				},	
				# {
				# 	'name': 'graph_bat_voltage',
				# 	'type': 'graph',
				# 	'save': True,
				# 	'title': 'Inverter - Battery voltage'
				# },
				# {
				# 	'name': 'graph_bat_current',
				# 	'type': 'graph',
				# 	'save': True,
				# 	'title': 'Inverter - Battery current'
				# },								
			]
		}	
		graphs_json = self.f_create_layout(graphs_json, type = 'vertical', group = 1)
		self.f_create_widget(graphs_json)				

	def create_front(self):
		self.create_root()
		self.create_frames()
		self.create_widgets()

		self.initialize()

	def recreate_front(self):
		self.root = None

		for frame in self.frames:
			self.frames[frame] = None
		
		for widget in self.widgets:
			self.widgets[widget] = None

		self.create_front()

	def f_create_widget(self, widgets_json, verbose = False):
		try:
			if widgets_json['layout']:
				set_layout = True
			else:
				set_layout = False
		except:
			set_layout = False
		
		if set_layout:
			layout = QGridLayout()

		# Base frame
		tmp_base_frame = self.frames[widgets_json['base_frame']]

		# Recorremos cada widget a añadir
		for i, widget in enumerate(widgets_json['list']):
				
			# #### Obtenemos la configuración
			# Save
			try:
				tmp_save = widget['save']
			except:
				tmp_save = True

			# ReadOnly
			try:
				tmp_readonly = widget['readonly']
			except:
				tmp_readonly = False

			# Width
			try:
				tmp_width = widget['width']
			except:
				if widget['type'] == 'frame':
					try:
						tmp_width = self.config['frames'][widget['name']]['width']
					except:
						tmp_width = self.config['frames']['width_default']
				else:
					tmp_width = self.config['widgets'][f"width_{widget['type']}"]
				
			# Height
			try:
				tmp_height = widget['height']
			except:
				if widget['type'] == 'frame':
					try:
						tmp_height = self.config['frames'][widget['name']]['height']
					except:
						tmp_height = self.config['frames']['height_default']				
				else:
					tmp_height = self.config['widgets'][f"height_{widget['type']}"]					

			# Background color
			try:
				tmp_background_color = widget['background-color']
			except:
				try:
					tmp_background_color = self.get_stylesheet(tmp_base_frame)['background-color']
				except Exception as e:
					tmp_background_color = self.config['frames']['default']['color']
			
			# Border style
			try:
				tmp_border_style = widget['border-style']
			except:
				if widget['type'] == "frame":
					tmp_border_style = self.config['frames']['default']['border-style']
				else:
					tmp_border_style = self.config['widgets']['borderstyle_none']
					# tmp_border_style = 'none'
	
			# Border width
			try:
				tmp_border_width = widget['border-width']
			except:
				tmp_border_width = self.config['frames']['default']['border-width']
			
			# Border radius
			try:
				tmp_border_radius = widget['border-radius']
			except:
				if widget['type'] == 'button':
					tmp_border_radius = self.config['widgets']['border_radius_button']
				else:
					tmp_border_radius = self.config['frames']['default']['border-radius']

			# Text	
			try:
				tmp_text = widget['text']
			except:
				tmp_text = ''

			# Fontsize
			try:
				tmp_fontsize = widget['fontsize']
			except:
				if widget['type'] == 'button':
					tmp_fontsize = self.config['widgets']['fontsize_button']
				else:
					tmp_fontsize = self.config['widgets']['fontsize_normal']

			# Fontweight
			try:
				tmp_fontweight = widget['font-weight']
			except:
				if widget['type'] == 'button':
					tmp_fontweight = self.config['widgets']['fontweight_bold']
				else:
					tmp_fontweight = self.config['widgets']['fontweight_normal']

			# Fontweigt
			try:
				tmp_fontweigth = widget['font-weight']
			except:
				tmp_fontweigth = self.config['widgets']['fontweight_normal']

			# #### CREATE widget -> f(type)
			if widget['type'] == 'frame':
				tmp_widget = QFrame(tmp_base_frame)
			elif widget['type'] == 'label':
				tmp_widget = QLabel(tmp_base_frame)
			elif widget['type'] == 'edit':
				# tmp_widget = QTextEdittmp_base_frame)
				tmp_widget = QLineEdit(tmp_base_frame)
			elif widget['type'] == 'combo':
				tmp_widget = QComboBox(tmp_base_frame)
				tmp_widget.addItems(widget['elements'])
			elif widget['type'] == 'button':
				tmp_widget = QPushButton(tmp_base_frame)
				# effect = QGraphicsEffect()
				tmp_widget.clicked.connect(widget['function'])
			elif widget['type'] == 'led':
				tmp_widget = QLed(tmp_base_frame, onColour = widget['on-color'], shape = widget['shape'])
				tmp_widget.value = True
			elif widget['type'] == 'image':
				tmp_widget = QLabel(tmp_base_frame)
				pixmap = QPixmap()
				tmp_widget.setPixmap(pixmap)
			elif widget['type'] == 'separator':
				tmp_widget = QLabel(tmp_base_frame)
			elif widget['type'] == 'graph':
				tmp_widget = pg.PlotWidget(tmp_base_frame)
				try:
					tmp_widget.setTitle(widget['title'])
				except:
					pass
					
			# Set readonly
			if tmp_readonly:
				tmp_widget.setReadOnly(True)

			# Set size
			try:
				tmp_widget.resize(tmp_width, tmp_height)
			except:
				pass

			# Set position or layout
			try:
				if set_layout:
					layout.addWidget(tmp_widget, widget['x'], widget['y'])
				else:
					tmp_widget.move(widget['x'], widget['y'])
			except:
				pass

			# Set style sheet and fonts
			try:
				if not widget['type'] == 'button':
					tmp_widget.setStyleSheet(
						f"background-color: {tmp_background_color};"
						f"border-style: {tmp_border_style};"
						f"border-style: {tmp_border_style};"
						f"border-width: {tmp_border_width};"
						f"border-radius: {tmp_border_radius};"
						f"font-size: {tmp_fontsize};"
						f"font-weight: {tmp_fontweight};"
					)
				else:
					tmp_widget.setStyleSheet(
						f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 white, stop: 0.8 {self.selected_colors['button']}, stop:1 black);"
						f"border-style: {tmp_border_style};"
						f"border-width: {tmp_border_width};"
						f"border-radius: {tmp_border_radius};"
						f"font-size: {tmp_fontsize};"
						f"font-weight: {tmp_fontweight};"					
					)
			except:
				pass

			# Set text
			try:
				tmp_widget.setText(tmp_text)
			except:
				pass

			# Save widget reference
			if tmp_save:
				if widget['type'] == 'frame':
					self.frames[widget['name']] = tmp_widget
				else:
					self.widgets[widget['name']] = tmp_widget

			# Verbose
			if verbose:
				print(f"Creating Widget \'{widget['name']}\' of type \'{widget['type']}\' (save = {tmp_save})")
				print(f" - Base frame: {widgets_json['base_frame']} ")
				print(f"  - x: {widget['x']}")
				print(f"  - y: {widget['y']}")
				print(f"  - Width: {tmp_width}")
				print(f"  - Height: {tmp_height}")
				print(f"  - Bg color: {tmp_background_color}")
				print(f"  - Border-style: {tmp_border_style}")
				print(f"  - Fontsize: {tmp_fontsize}")
				print(f"  - Font-weight: {tmp_fontweigth}")

		# Set frame layout if selected
		if set_layout:
			layout.setContentsMargins(self.config['layouts']['widget_margin_left'], self.config['layouts']['widget_margin_top'], self.config['layouts']['widget_margin_right'], self.config['layouts']['widget_margin_bottom'])
			tmp_base_frame.setLayout(layout)

	def f_create_layout(self, json, type = 'vertical', init_x = -1, init_y = -1, spacing_x = -1, spacing_y = -1, group = 1, verbose = False):
			
		base_frame = json['base_frame']

		# init_x
		if init_x == -1:
			try:
				init_x = self.config['frames'][base_frame]['init_x']
			except:
				init_x = self.config['frames']['default']['init_x']		

		# init_y
		if init_y == -1:
			try:
				init_y = self.config['frames'][base_frame]['init_y']
			except:
				init_y = self.config['frames']['default']['init_y']				
		# spacing_x
		if spacing_x == -1:
			try:
				spacing_x = self.config['frames'][base_frame]['spacing_x']
			except:
				spacing_x = self.config['frames']['default']['spacing_x']					
		# spacing_y
		if spacing_y == -1:
			try:
				spacing_y = self.config['frames'][base_frame]['spacing_y']
			except:
				spacing_y = self.config['frames']['default']['spacing_y']					

		if not len(json['list']) % group == 0:
			print("Cannot create layout")
		else:
			# Inicializamos x e y
			tmp_x = init_x
			tmp_y = init_y

			for i in range(0, len(json['list']), group):
				if type == 'vertical':
					tmp_x = init_x
					tmp_y = tmp_y
				elif type == 'horizontal':
					tmp_x = tmp_x
					tmp_y = init_y					  
				
				max_width = 0
				max_height = 0
				for j in range(0, group):
					# Obtenemos el widget objetivo de la lista
					it = i+j
					tmp = json['list'][it]

					# Width
					try:
						tmp_width = tmp['width']
					except:
						if tmp['type'] == 'frame':
							tmp_width = self.config['frames'][tmp['name']]['width']
						else:
							tmp_width = self.config['widgets'][f"width_{tmp['type']}"]

					# Save maximum width of group
					max_width = max([max_width, tmp_width])

					# Height
					try:
						tmp_height = tmp['height']
					except:
						if tmp['type'] == 'frame':
							tmp_height = self.config['frames'][tmp['name']]['height']
						else:
							tmp_height = self.config['widgets'][f"height_{tmp['type']}"]

					# Save maximum height of group
					max_height = max([max_height, tmp_height])

					# Check for x and y modifiers 
					try:
						tmp_delta_x = tmp['delta_x']
					except:
						tmp_delta_x = 0

					try:
						tmp_delta_y = tmp['delta_y']
					except:
						tmp_delta_y = 0


					# Assign current x and y values
					json['list'][it]['x'] = tmp_x + tmp_delta_x
					json['list'][it]['y'] = tmp_y + tmp_delta_y

					if verbose:
						print(f"Placing widget {i+j} -> {tmp['name']} ({tmp['type']})")
						print(f"  - x: {tmp_x} (width = {tmp_width})")
						print(f"  - y: {tmp_y} (height = {tmp_height})")
					
					# Recalculamos el valor de x
					if type == 'vertical':
						tmp_x = tmp_x + tmp_width + spacing_x
					else:
						tmp_y = tmp_y + tmp_height + spacing_y
	
				# Recalculamos el valor de y
				if type == 'vertical':
					tmp_y = tmp_y + max_height + spacing_y
				else:
					tmp_x = tmp_x + max_width + spacing_x
		
		return json
	
	def get_stylesheet(self, widget):
		try:
			tmp = list(map(lambda x: x.split(':'), widget.styleSheet().split(';')))

			keys = []
			values = []
			for item in tmp:
				try:
					new_key = item[0]
					new_value = item[1]

					keys.append(new_key)
					values.append(new_value)
				except:
					pass

			ret_val = dict.fromkeys(keys, values)

		except Exception as e:
			print(f"GetStyle: {e}")
			ret_val = None

		return ret_val

	def initialize(self):
		data = {
				'window': {
					'message': "Disconnected from server...",
					'message_alt': '',
					'setpoint_val': 0,
					'setpoint_dir': 'Rest',
					'running_order': False,
				},
				'test': {
					'ok': False,
					'running': False,
					'finished': False,
					'path': 'Not loaded...',
				},
				'comms_inverter': {
					'inverter': 'SMA',
					'connected': False,
					'ip': '192.168.55.243',
					# 'ip': '192.168.1.200',
					'port': 502,
					'uid': 3,
				},
				'comms_battery': {
					'inverter': 'Cegasa',
					'connected': False,
					'ip': '192.168.55.11',
					'port': 502,
					'uid': 1,
				},				
				'inverter': {
					'manufacturer': '---',
					'model': '---',
					'serial': '---',
					'status': '---',
					'operation': '---',
					'running': False,
					'power_3': '---',
					'power_r': '---',
					'power_s': '---',
					'power_t': '---',
					'bat_voltage': '---',
					'bat_current': '---',
					'bat_soc': '---',
				},
				'battery': {
					'status': '---',
					'soc': '---',
					'voltage': '---',
					'current': '---',
					'ch_current': '---',
					'dsch_current': '---',
					'ch_voltage': '---',
					'dsch_voltage': '---',
				}
			}

		self.update_values(data)

		self.widgets['manufacturer_inv'].setCurrentText(data['comms_inverter']['inverter'])
		self.widgets['ip_inv'].setText(data['comms_inverter']['ip'])
		self.widgets['port_inv'].setText(str(data['comms_inverter']['port']))
		self.widgets['uid_inv'].setText(str(data['comms_inverter']['uid']))

		self.widgets['manufacturer_bat'].setCurrentText(data['comms_battery']['inverter'])
		self.widgets['ip_bat'].setText(data['comms_battery']['ip'])
		self.widgets['port_bat'].setText(str(data['comms_battery']['port']))
		self.widgets['uid_bat'].setText(str(data['comms_battery']['uid']))

		self.config['init']['initialized'] = True
			
	def connect(self):
		self.set_comms()

		if not self.values['comms_inverter']['connected']:
			self.config['MVC']['controller'].connect()

			sleep(1)

			if self.values['comms_inverter']['connected']:
				self.config['MVC']['controller'].start_comm()
				self.values['comms_inverter']['autocomm'] = True
				
		else:
			if self.values['comms_inverter']['connected']:
				self.config['MVC']['controller'].stop_comm()    			
				self.values['comms_inverter']['autocomm'] = False

			sleep(1)

			self.config['MVC']['controller'].disconnect()

	def run(self):
		if not self.values['inverter']['running']:
			self.config['MVC']['controller'].op_inverter(action = 'run')
		else:
			self.config['MVC']['controller'].op_inverter(action = 'stop')

	def check_test(self):
		self.set_message("Checking test...")

		valid_type = "json"
		try:
			path = str(pathlib.Path().resolve())

			options = QFileDialog.Options()
			test_file = QFileDialog.getOpenFileName(parent = None, caption = "Select test file", directory = path, filter = f"Test files (*.{valid_type})", options = options)[0]

			# Check if selected file is valid
			if test_file.split('/')[-1].split(".")[-1] == valid_type:
				# If is, check the test
				self.config['MVC']['controller'].check_test(test_file)
			else:
				# If not, send message to user
				message = "This is not a valid file..."
				self.set_message(message)
		except:
			pass

			message = "Something was wrong loading test file..."	
			self.set_message(message)
			
	def run_test(self):
		if self.values['comms_inverter']['connected']:
			if not self.values['test']['running']:
				self.config['MVC']['controller'].start_test()
			else:
				self.config['MVC']['controller'].stop_test()
		else:
			self.set_message('Cannot start test while not connected...')

	def update_values(self, data = None):
		if not data == None:
			for key, values in data.items():
				for key_value, value in values.items():
					if type(value) == bool:	
						self.values[key][key_value] = value
					else:
						self.values[key][key_value] = str(value)
		
		self.publish()
	
	def publish(self, verbose = False):
		# WINDOW
		try:
			self.widgets['message'].setText(self.values['window']['message'])
			self.widgets['setpoint_type'].setText(f"{self.values['window']['setpoint_type']} setpoint")
			self.widgets['setpoint_indicator'].setText(f"  {self.values['window']['setpoint_indicator']}")
		except Exception as e:
			pass

		# CONNECTION
		# Inverter
		self.widgets['conn_state_inv'].value = self.values['comms_inverter']['connected']
		if self.values['comms_inverter']['connected']:
			self.widgets['connect'].setText('Disconnect')
		else:
			self.widgets['connect'].setText('Connect')

		if self.values['comms_inverter']['connected']:
			self.widgets['manufacturer_inv'].setCurrentText(self.values['comms_inverter']['manufacturer'])
			self.widgets['ip_inv'].setText(self.values['comms_inverter']['ip'])
			self.widgets['port_inv'].setText(self.values['comms_inverter']['port'])
			self.widgets['uid_inv'].setText(self.values['comms_inverter']['uid'])

		self.widgets['run_state_inv'].value = self.values['inverter']['running']
		if self.values['inverter']['running']:
			self.widgets['run'].setText('Stop')
		else:
			self.widgets['run'].setText('Run')

		# Battery
		self.widgets['conn_state_bat'].value = self.values['comms_battery']['connected']
		if self.values['comms_battery']['connected']:
			self.widgets['manufacturer_bat'].setCurrentText(self.values['comms_battery']['manufacturer'])
			self.widgets['ip_bat'].setText(self.values['comms_battery']['ip'])
			self.widgets['port_bat'].setText(self.values['comms_battery']['port'])
			self.widgets['uid_bat'].setText(self.values['comms_battery']['uid'])

		if verbose:
			print("\nCONNECTION:")
			print(" * INVERTER")
			print(f"  - Connection status: {self.values['comms_inverter']['connected']}")
			print(f"  - Ip: {self.values['comms_inverter']['ip']}")
			print(f"  - Port: {self.values['comms_inverter']['port']}")
			print(f"  - Uid: {self.values['comms_inverter']['uid']}")
			print(" * BATTERY")
			print(f"  - Connection status: {self.values['comms_battery']['connected']}")
			print(f"  - Ip: {self.values['comms_battery']['ip']}")
			print(f"  - Port: {self.values['comms_battery']['port']}")
			print(f"  - Uid: {self.values['comms_battery']['uid']}")		

		# TEST
		try:
			self.widgets['test_path'].setText(self.values['test']['path'].split('/')[-1])
		except:
			self.widgets['test_path'].setText('Not loaded...')

		self.widgets['test_ok'].value = abs(int(self.values['test']['ok']))

		# Cambiamos el valor y color del led test_running
		self.widgets['test_running'].value = (self.values['test']['running']) or (self.values['test']['finished'])
		if not self.values['test']['finished']:
			self.widgets['test_running'].onColour = QLed.Green
		else:
			self.widgets['test_running'].onColour = QLed.Red
			
		try:
			self.widgets['test_time'].setText(self.values['test']['total_time'].split('.')[0])
		except Exception as e:
			self.widgets['test_time'].setText('0')

		self.widgets['test_it'].setText(f"{self.values['test']['it']} of {self.values['test']['total_it']}")
		
		# Change test run button text
		if self.values['test']['running']:
			self.widgets['test_run'].setText('Stop')
		else:
			self.widgets['test_run'].setText('Run')
		
		# Change test ok led color depending on self.values['test']['ok']		
		if not int(self.values['test']['ok']) == -1:
			# If it's 0 (init) or 1 (ok)
			self.widgets['test_ok'].onColour = QLed.Green
		else:
			# If it's -1 (nok)
			self.widgets['test_ok'].onColour = QLed.Red

		# INVERTER
		self.widgets['run_state_inv'].value = self.values['inverter']['running']
		self.widgets['manufacturer'].setText(self.values['inverter']['manufacturer'])
		self.widgets['model'].setText(self.values['inverter']['model'])
		self.widgets['serial'].setText(self.values['inverter']['serial'])
		self.widgets['status_inv'].setText(self.values['inverter']['status'])
		self.widgets['power_3_inv'].setText(self.values['inverter']['power_3'])
		self.widgets['power_r_inv'].setText(self.values['inverter']['power_r'])
		self.widgets['power_s_inv'].setText(self.values['inverter']['power_s'])
		self.widgets['power_t_inv'].setText(self.values['inverter']['power_t'])
		self.widgets['voltage_inv'].setText(self.values['inverter']['bat_voltage'])
		self.widgets['current_inv'].setText(self.values['inverter']['bat_current'])
		self.widgets['soc_inv'].setText(self.values['inverter']['bat_soc'])

		# BATTERY
		self.widgets['status_bat'].setText(self.values['battery']['status'])
		self.widgets['soc_bat'].setText(self.values['battery']['soc'])
		self.widgets['voltage_bat'].setText(self.values['battery']['voltage'])
		self.widgets['current_bat'].setText(self.values['battery']['current'])
		self.widgets['ch_current_bat'].setText(self.values['battery']['ch_current'])
		self.widgets['dsch_current_bat'].setText(self.values['battery']['dsch_current'])
		self.widgets['ch_voltage_bat'].setText(self.values['battery']['ch_voltage'])
		self.widgets['dsch_voltage_bat'].setText(self.values['battery']['dsch_voltage'])

	def get_values(self):
		return self.values

	def update_setpoint(self):
		self.config['MVC']['controller'].set_manual_setpoint(self.get_manual_setpoint())

	def plot_graph_power(self, data):
		data_x = data['x'].values
		data_y = data['y'].values
		data_y_sp = data['y_sp'].values		

		try:
			for power_line in self.power_line:
				try:
					power_line.clear()
				except:
					pass
		except:
			pass

		# self.power_line = []
		# self.power_line.append(self.widgets['graph_power'].plot(data_y, pen=pg.mkPen('w', width = 4)))
		# self.power_line.append(self.widgets['graph_power'].plot(data_y_sp, pen=pg.mkPen('r', width = 4)))

		# hour = [1,2,3,4,5,6,7,8,9,10]
		# temperature = [30,32,34,32,33,31,29,32,35,45]

		# temperature = []
		# for i in range(len(hour)):
		# 	temperature.append(50 + random.uniform(-20, 20))

		# self.line = self.widgets['graph_power'].plot(data_x, data_y)
		# self.line = self.widgets['graph_power'].plot(hour, temperature)

		# self.widgets['graph_power'].plot(data['x'], data['y'])
    		# for p in data:
			# self.widgets['graph_power'].plot(p['x'], p['y'])
		    		
	def plot_graph_bat_soc(self, data):
		# for p in data:
		# 	self.widgets['graph_bat_soc'].plot(p['x'], p['y'])
		data_x = data['x'].values
		data_y = data['y'].values

		try:
			self.bat_soc_line.clear()
		except:
			pass

		# self.bat_soc_line = None
		# self.bat_soc_line = self.widgets['graph_bat_soc'].plot(data_y)

	def plot_graph_bat_voltage(self, data):
		# for p in data:
		# 		self.widgets['graph_bat_voltage'].plot(p['x'], p['y'])    		
		data_x = data['x'].values
		data_y = data['y'].values

		try:
			self.bat_voltage_line.clear()
		except:
			pass

		self.bat_voltage_line = None
		self.bat_voltage_line = self.widgets['graph_bat_voltage'].plot(data_y)

	def plot_graph_bat_current(self, data):
		# for p in data:
		# 	self.widgets['graph_bat_current'].plot(p['x'], p['y'])    		

		data_x = data['x'].values
		data_y = data['y'].values

		try:
			self.bat_current_line.clear()
		except:
			pass

		self.bat_current_line = None
		self.bat_current_line = self.widgets['graph_bat_current'].plot(data_y)

	def get_manual_setpoint(self):
		try:
			tmp_val = int(self.widgets['setpoint_val'].text())
		except:
			tmp_val = 0
		
		try:
			tmp_dir = self.widgets['setpoint_dir'].currentText()
		except:
			tmp_dir = 'Rest'

		setpoint = {
			'val': tmp_val,
			'dir': tmp_dir,
		}

		return setpoint

	def set_message(self, message):
		tmp_values = self.get_values()
		tmp_values['window']['message'] = message
		self.update_values(tmp_values)

	def run_app(self):
		self.root.show()
		self.exec()

	def exit(self):
		self.config['MVC']['controller'].stop_app()
