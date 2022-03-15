import sys
import trace
import threading
import json
from datetime import date, datetime, timedelta
from time import sleep

import pandas as pd

import random

from controller.modbus_sma import sma
from controller.modbus_victron import victron
from controller.modbus_ingeteam import ingeteam

import paho.mqtt.client as paho

# from controller.modbus import Modbus
# from modbus_cegasa import cegasa


class Controller():
	# ################## INIT ##################    	
	def __init__(self) -> None:
		# CONFIG
		self.config = {}
		self.create_config()
		self.initialize_config()

		# THREADS
		self.threads = []
		self.config_thread()
		self.create_thread_manager()

		# COMMS
		self.create_comms_manager()

		# MQTT
		self.mqtt_connect()

		# TEST
		self.test = {}
		self.create_test_manager()


	# ################## THREADS ##################
	# ###### THREAD MANAGER ######
	def thread_manager(self):
		print(f"{self.get_now()}: Thread manager created!")

		self.config['threads']['it'] = 0
		elapsed_time = 0

		start_time  = datetime.now()
		it_end_time = start_time
		while self.config['app']['running']:
			# Update iteration
			self.config['threads']['it'] += 1

			# Update iteration starting time
			it_start_time = it_end_time

			# Show current threads
			# self.show_threads()

			# Updating threads is_alive status
			self.update_threads()

			# Clear not alive's threads
			self.clear_threads()

			# Sleep
			thr = self.get_thread(name = 'thread_manager')
			sleep(thr['timing'])

			# Update iteration ending, iteration and elapsed time
			it_end_time = datetime.now()
			self.config['threads']['elapsed_time'] = (it_end_time - start_time)
			self.config['threads']['iteration_time'] = (it_end_time - it_start_time)
		
		print(f"{self.get_now()}: Thread manager exited!")

	def create_thread(self, target = None, name = '', desc = '', verbose = False):
		try:
			new_desc = desc

			if name == '':
				new_name = f'thread_{len(self.threads)}'
			else:
				new_name = name
			
			# Buscamos el nombre
			if not new_name in self.config['threads']['names']:
				# Si no esta, lo agregamos y continuamos
				self.config['threads']['names'].append(new_name)
			else:
				# Si esta, añadimos números hasta tener un nombre único
				cont = 1
				while new_name in self.config['threads']['names']:
					new_name += f'_{str(cont)}'

					cont += 1

			# Elegimos el timing
			try:
				new_timing = self.config['threads']['timing'][new_name]
			except:
				new_timing = self.config['threads']['timing']['default']

			# Creamos el hilo
			new_ref = inner_thread(target = target)

			# Cremos la nueva estructura del hilo
			new_thread = {
				'alive': new_ref.is_alive(),
				'id': self.config['threads']['count'],
				'name': new_name,
				'desc': new_desc,
				'ref': new_ref,
				'not_alive_counter': 0,
				'timing': new_timing, 
			}
			self.threads.append(new_thread)
			self.config['threads']['count'] += 1

			new_ref.start()

			# Verbose
			if verbose:
				print(f"Total thread number: {len(self.threads)}")
				print("  Creating thread...")
				for key, value in new_thread.items():
					print(f"   * {key} -> {value}")
		except:
			print(f"Failed creating thread {name}")

	def create_thread_manager(self):
		self.create_thread(target = self.thread_manager, name = 'thread_manager', desc = 'THREAD MANAGER')

	def create_comms_manager(self):
		self.create_thread(target = self.comms_manager, name = 'comms_manager', desc = 'COMMS MANAGER for INVERTER')

	def create_test_manager(self):
		self.create_thread(target = self.test_manager, name = 'test_manager', desc = 'TEST MANAGER')
	
	def config_thread(self):
		self.config['threads'] = {}

		self.config['threads']['names'] = []
		self.config['threads']['count'] = 0
		self.config['threads']['elapsed_time'] = None
		self.config['threads']['iteration_time'] = None
		self.config['threads']['it'] = 0

		self.config['threads']['timing'] = {}
		self.config['threads']['timing']['default'] = 5
		self.config['threads']['timing']['thread_manager'] = 2
		self.config['threads']['timing']['comms_manager'] = 2
		self.config['threads']['timing']['test_manager'] = 2

	def update_threads(self):
		# Updating each thread "is_alive"
		for i, thr in enumerate(self.threads):
			thr['alive'] = thr['ref'].is_alive()

			if thr['alive']:
				thr['not_alive_counter'] = 0
			else:
				thr['not_alive_counter'] += 1
	
	def clear_threads(self):
		not_alives_threslhold = 3

		# Clearing not alive's threads
		for i, thr in enumerate(self.threads):
			if thr['not_alive_counter'] >= not_alives_threslhold:
				self.threads.pop(i)
		
		# Updating threads counter
		self.config['threads']['count'] = len(self.threads)

	def show_threads(self):
		print("\n#############################################\n")
		print(f" ITERATION {self.config['threads']['it']} (Total {self.config['threads']['elapsed_time']}, iteration on {self.config['threads']['iteration_time']})\n")
		print(f" {len(self.threads)} threads")
		for i, thr in enumerate(self.threads):
			try:
				print(f"  - Thread {i}: {thr['name']} -> {thr['ref']} / Alive: {thr['alive']} ({thr['not_alive_counter']} not alives)")
			except:
				print(f"  - Thread {i}: Fail")
		print("\n#############################################")
		print("#############################################\n")

	def get_thread(self, name = ''):
		ret_val = None

		if not name == '':
			for thr in self.threads:
				if thr['name'] == name:
					ret_val = thr
					break
			
		return ret_val
					

	# Specific methods
	def start_comm(self, verbose = False):
		self.config['comms']['inverter']['comm'] = True

		# self.create_thread(target = self.comm, name = 'comm_loop', desc = 'MODBUS Communication loop')

		if verbose:
			print(f"Starting thread with \"name\" = \"comm_loop\"...")		

	def stop_comm(self, verbose = False):
		self.config['comms']['inverter']['comm'] = False

		# self.kill_thread_by_name(name = 'comm_loop', match = False, verbose = True)

		if verbose:
			print(f"Killing all threads with \"name\" = \"comm_loop\"...")
		
	def get_ref_by(self, param = '', value = 0):
		ret_val = None
		
		if not param == '':
			for thr in self.threads:
				try:
					if thr[param] == value:
						ret_val = thr['ref']
						break
				except:
					pass
			
		return ret_val

	def kill_thread(self, param = '', value = 0, verbose = False):
		for thr in self.threads:
			try:
				if thr[param] == value:
					if verbose:
						print(f"\nKilling thread:")
						print(f" - Id: {thr['id']}")
						print(f" - Name: {thr['name']}")
						print(f" - Desc: {thr['desc']}")

					ref = self.get_ref_by(param = param, value = value)

					ref.kill()
			except:
				pass

	def kill_thread_by_name(self, name = 0, match = False, verbose = False):
		for i, thr in enumerate(self.threads):
				
			# Buscamos en el nombre del hilo
			if thr['name'] == name:
				if verbose:
					print(f"\nKilling thread:")
					print(f" - Id: {thr['id']}")
					print(f" - Name: {thr['name']}")
					print(f" - Desc: {thr['desc']}\n")

				# Obtenemos la referencia del hilo
				ref = self.get_ref_by(param = 'name', value = name)

				# Matamos el hilo
				ref.kill()

				# Esperamos a que termine
				ref.join()

				# Elimilnamos el hilo de la lista
				self.threads = self.threads.pop(i)

	def kill_all_threads(self, verbose = False):
		if verbose:
			print("Killing threads...")
		for thr in self.threads:
			if verbose:
				print(f"  Killing thread {thr['id']} {thr['name']}...")
			
			self.kill_thread('id', thr['id'])

		if verbose:
			print("All threads killed!")
	


	# ################## CONFIG ##################
	def create_config(self):
		self.config = {
			'app': {},
			'MVC':  {},
			'threads': {},
			'scale': {},
			'comms': {},
			'mqtt': {},
		}

	def initialize_config(self):
		# APP
		self.config['app']['running'] = True
		self.config['app']['initialized'] = False
		self.config['app']['error'] = False

		# MVC REF
		self.config['MVC']['components'] = ['model', 'view', 'controller']
		self.config['MVC']['model'] = None
		self.config['MVC']['view'] = None
		self.config['MVC']['controller'] = None

		# SCALE
		self.config['scale']['abs'] = None
		self.config['scale']['x']   = None
		self.config['scale']['y']   = None

		# COMMS
		self.config['comms']['inverter'] = {
			'ref': None,
			'ip': None,
			'port': None,
			'uid': None,
			'manufacturer': None,
			'connected': False,
			'running': False,
			'setpoint_val': 0,
			'setpoint_dir': 'rest',
			'manual_setpoint_val': 0,
			'manual_setpoint_dir': 'rest',
		}
		self.config['comms']['battery'] = {
			'ref': None,
			'ip': None,
			'port': None,
			'uid': None,			
			'manufacturer': None,
			'connected': False,
			'running': False,
		}
		self.config['comms']['default'] = {
			'ip': '192.168.1.10',
			'port': 502,
			'uid': 1,			
		}

		# MQTT
		self.config['mqtt']	= {}
		self.config['mqtt']['broker'] = '192.168.55.3'
		self.config['mqtt']['port'] = 1883
		self.config['mqtt']['topic'] = 'kaiola/data'

		# TEST
		self.test = {
			'file': None,
			'checked': False,
			'running': False,
			'finished': False,
			'check': None, 
			'name': None,
			'starting_time': None,
			'iterations': None,
			'n_steps': None,
			'total_steps': None,
			'base_time': None,
			'sleeping_val': None,
			'sleeping_dir': None,
			'profile': None,
			'setpoint_val': None,
			'setpoint_dir': None,
			'total_time': None,
			'it': None,
		}

		# Read data
		self.read_data = {}
		self.read_data['config'] = {}
		self.read_data['config'] = {
			'max_points': 200,
		}

		self.read_data = {
			'timestamp': [],
			'power_setpoint': [],
			'power_3': [],
			'bat_soc': [],
			'bat_voltage': [],
			'bat_current': [],
		}

		self.update_setpoint()

	def set_mvc_refs(self, data, verbose = False):
		for mvc in data:
				if mvc in self.config['MVC']['components']:
					if mvc == "controller":
						self.config['MVC'][mvc] = self
					else:
						self.config['MVC'][mvc] = data[mvc]

		# Pasamos las referencias a MODEL
		self.config['MVC']['model'].set_mvc_refs(data, verbose = verbose)
		# Pasamos las referencias a VIEW
		self.config['MVC']['view'].set_mvc_refs(data, verbose = verbose)

		if verbose:
			print("Controller MVC refs changed!")
			print(f"  - Model: 		{self.config['MVC']['model']}")
			print(f"  - View: 		{self.config['MVC']['view']}")
			print(f"  - Controller: {self.config['MVC']['controller']}")

	def set_scale(self, data, verbose = False):
		self.config['scale']['abs'] = data['abs']

		self.config['scale']['x'] = self.config['scale']['abs']
		self.config['scale']['y'] = self.config['scale']['abs']

		self.config['MVC']['view'].set_scale(data)

		if verbose:
			self.show_scale()
			self.config['MVC']['view'].show_scale()

	def show_scale(self):
		print("\Controller scale:")
		print(f"  - Abs: {self.config['scale']['abs']}")
		print(f"  - x: {self.config['scale']['x']}")
		print(f"  - y: {self.config['scale']['y']}")

	# #################### COMMS ####################
	# ###### COMMS MANAGER ######
	def comms_manager(self):
		print(f"{self.get_now()}: Comms manager created!")

		self.config['comms']['it'] = 0
		elapsed_time = 0

		start_time  = datetime.now()
		it_end_time = start_time

		while self.config['app']['running']:
			# INVERTER CONNECTION
			self.check_comm_inverter()

			if self.config['comms']['inverter']['connected']:
				self.comm_inverter()

			# BATTERY CONNECTION
			self.check_comm_battery()

			if self.config['comms']['battery']['connected']:
				self.comm_battery()

			self.update_connection_status()

			# Sleep
			thr = self.get_thread(name = 'comms_manager')
			sleep(thr['timing'])

		print(f"{self.get_now()}: Comms manager exited!")			

	def set_comms(self, data):
		# INVERTER IP
		try:
			self.config['comms']['inverter']['ip'] = data['inverter']['ip']
		except:
			pass
		# INVERTER PORT
		try:
			self.config['comms']['inverter']['port'] = data['inverter']['port']
		except:
			pass
		# INVERTER UID
		try:
			self.config['comms']['inverter']['uid'] = data['inverter']['uid']
		except:
			pass
		# INVERTER MANUFACTURER
		try:
			self.config['comms']['inverter']['manufacturer'] = data['inverter']['manufacturer']
		except:
			pass	

		# BATTERY IP
		try:
			self.config['comms']['battery']['ip'] = data['battery']['ip']
		except:
			pass
		# BATTERY PORT
		try:
			self.config['comms']['battery']['port'] = data['battery']['port']
		except:
			pass
		# BATTERY UID
		try:
			self.config['comms']['battery']['uid'] = data['battery']['uid']
		except:
			pass
		# BATTERY MANUFACTURER
		try:
			self.config['comms']['battery']['manufacturer'] = data['battery']['manufacturer']
		except:
			pass				

	def show_comms(self):
		print("\nINVERTER:")
		for key, value in self.config['comms']['inverter'].items():
			print(f"{key} -> {value}")

		print("\nBATTERY:")
		for key, value in self.config['comms']['battery'].items():
			print(f"{key} -> {value}")			

	def connect(self):
		ip = self.config['comms']['inverter']['ip']
		port = self.config['comms']['inverter']['port']
		uid = self.config['comms']['inverter']['uid']

		# Choose Modbus instance depending on inverter manufacturer
		if self.config['comms']['inverter']['manufacturer'] == 'SMA':
			self.config['comms']['inverter']['ref'] = sma(ip, port, uid, self.config['comms']['inverter']['manufacturer'])
			# self.config['comms']['inverter']['ref'] = Modbus(ip, port, uid)
		elif self.config['comms']['inverter']['manufacturer'] == 'Ingeteam':
			self.config['comms']['inverter']['ref'] = ingeteam(ip, port, uid, self.config['comms']['inverter']['manufacturer'])
			
		# elif self.config['comms']['inverter']['manufacturer'] == 'Victron':
		# 		self.config['comms']['inverter']['ref'] = victron(ip, port, uid, self.config['comms']['inverter']['manufacturer'])

		self.config['comms']['inverter']['connected'] = self.config['comms']['inverter']['ref'].get_connection_status()

		self.update_connection_status()

	def disconnect(self):
		try:	
			self.config['comms']['inverter']['ref'].disconnect()
		except:
			pass

		self.config['comms']['inverter']['comm'] = False

		self.update_connection_status()

	def update_connection_status(self, error = False):
			ip = self.config['comms']['inverter']['ip']
			port = self.config['comms']['inverter']['port']
			uid = self.config['comms']['inverter']['uid']	

			# Creamos mensaje de salida
			if self.config['comms']['inverter']['connected']:
				message = f"Connection established with {ip}:{port} ({uid})"
			else:
				if not error:
					message = f"Disconnected from server with {ip}:{port} ({uid})..."
				else:
					message = f"Disconnected from server {ip}:{port} due to an error..."
			# Escribimoms mensaje de salida
			try:
				self.config['MVC']['view'].set_message(message)
			except:
				pass

			# Actualizamos valor del estado de la conexión
			try:
				tmp_values = self.config['MVC']['view'].get_values()
				tmp_values['comms_inverter']['connected'] = self.config['comms']['inverter']['connected']
				tmp_values['comms_battery']['connected'] = self.config['comms']['battery']['connected']

				self.config['MVC']['view'].update_values(tmp_values)
			except:
				pass

	def check_comm_inverter(self):
		try:	
			self.config['comms']['inverter']['connected'] = self.config['comms']['inverter']['ref'].get_connection_status()
		except:
			self.config['comms']['inverter']['connected'] = False

	def comm_inverter(self):
		self.comm_inverter_read()
	
		sleep(1)

		self.comm_inverter_write()

	def comm_inverter_read(self):
		# READ INVERTER
		try:
			tmp_values = self.config['MVC']['view'].get_values()

			# Leemos los valores de inverter
			tmp_dataset = self.config['comms']['inverter']['ref'].read()

			# Reemplazamos los valores de inverter recien leidos que no sean None
			for key, value in tmp_dataset['inverter'].items():
				try:
					if not value is None:
						tmp_values['inverter'][key] = value
				except:
					pass

			# Escribimos los valores actuales 
			self.config['MVC']['view'].update_values(tmp_values)

			# # Guardamos los valores a graficar y los mostramos
			# self.get_graph_data(tmp_dataset)
			# self.publish_graph_data()

			# Publicamos en MQTT la potencia leida
			self.mqtt_publish(data = tmp_values['inverter']['power_3'])


		except:
			pass

	def comm_inverter_write(self):
    	#  WRITE INVERTER
		try:
			self.update_setpoint()
		except:
			pass

	def get_graph_data(self, dataset):
		try:
			new_timestamp = dataset['timestamp']
			# new_timestamp = dataset['timestamp'].strftime('%Y/%m/%d %H:%M%S')
			# new_power = dataset['inverter']['power_3']
			# new_soc = round(dataset['inverter']['bat_soc']
			# new_voltage = round(dataset['inverter']['bat_voltage']
			# new_current = round(dataset['inverter']['bat_current']
			# new_power = round(dataset['inverter']['power_3'] + random.uniform(-100.0, 100.0), 2)

			# print(f"x: {new_timestamp} / y: {new_power}")

			# self.read_data['config']['max_points']
			# max_points = self.read_data['config']['max_points']
			max_points = 200

			if len(self.read_data['timestamp']) >= max_points:
				self.read_data['timestamp'] = self.read_data['timestamp'][1:]
				self.read_data['power_setpoint'] = self.read_data['power_setpoint'][1:]
				self.read_data['power_3'] = self.read_data['power_3'][1:]
				self.read_data['bat_soc'] = self.read_data['bat_soc'][1:]
				# self.read_data['bat_voltage'] = self.read_data['bat_voltage'][1:]
				# self.read_data['bat_current'] = self.read_data['bat_current'][1:]

			tmp_setpoint = self.config['comms']['inverter']['setpoint_val']
			if self.config['comms']['inverter']['setpoint_dir'].lower() == 'charge':
				tmp_setpoint = (-1) * tmp_setpoint
			elif self.config['comms']['inverter']['setpoint_dir'].lower() == 'rest':
				tmp_setpoint = 0

			self.read_data['timestamp'].append(new_timestamp)
			self.read_data['power_setpoint'].append(tmp_setpoint)
			self.read_data['power_3'].append(dataset['inverter']['power_3'])
			self.read_data['bat_soc'].append(dataset['inverter']['bat_soc'])
			# self.read_data['bat_voltage'].append(dataset['inverter']['bat_voltage'])
			# self.read_data['bat_current'].append(dataset['inverter']['bat_current'])

		except Exception as e:
			print("Failed in get_graph_data")
			print(e)

	def publish_graph_data(self):
		try:
			data = pd.DataFrame()

			data['x'] = pd.to_datetime(self.read_data['timestamp'])

			# Power
			data['y'] = self.read_data['power_3']
			data['y_sp'] = self.read_data['power_setpoint']
			self.config['MVC']['view'].plot_graph_power(data)

			# SoC
			data['y'] = self.read_data['bat_soc']
			data['y_sp'] = None
			self.config['MVC']['view'].plot_graph_bat_soc(data)

			# # Voltage
			# data['y'] = self.read_data['bat_voltage']
			# data['y_sp'] = None
			# self.config['MVC']['view'].plot_graph_bat_voltage(data)

			# # Current
			# data['y'] = self.read_data['bat_current']
			# data['y_sp'] = None
			# self.config['MVC']['view'].plot_graph_bat_current(data)

		except Exception as e:
			print("Failed in publish_graph_data")
			print(e)

	def set_manual_setpoint(self, setpoint):
		self.config['comms']['inverter']['manual_setpoint_val'] = setpoint['val']
		self.config['comms']['inverter']['manual_setpoint_dir'] = setpoint['dir']
    	
	def update_setpoint(self):
		# Inicializamos las variables
		# Obtenemos los setpoint manuales
		try:
			tmp_manual_val = self.config['comms']['inverter']['manual_setpoint_val']
			tmp_manual_dir = self.config['comms']['inverter']['manual_setpoint_dir']
		except:
			tmp_manual_val = 0
			tmp_manual_dir = 'rest'

		# Obtenemos los setpoint test
		try:
			tmp_test_val = self.test['setpoint_val']
			tmp_test_dir = self.test['setpoint_dir']
		except:
			tmp_test_val = 0
			tmp_test_dir = 'rest'
		
		# Escogemos el correspondiente setpoint
		try:
			test_running = self.test['running']
			test_finished = self.test['finished']
		except:
			test_running = False
			test_finished = False

		if test_running or test_finished:
			self.config['comms']['inverter']['setpoint_val'] = tmp_test_val
			self.config['comms']['inverter']['setpoint_dir'] = tmp_test_dir

			tmp_setpoint_type = 'Testing'
		else:
			self.config['comms']['inverter']['setpoint_val'] = tmp_manual_val
			self.config['comms']['inverter']['setpoint_dir'] = tmp_manual_dir

			tmp_setpoint_type = 'Manual'

		self.send_setpoint()
		self.publish_setpoint(tmp_setpoint_type)

	def send_setpoint(self):
		if self.config['comms']['inverter']['connected']:
			if self.config['comms']['inverter']['setpoint_dir'].lower() == 'charge':
				self.config['comms']['inverter']['ref'].setCharging(self.config['comms']['inverter']['setpoint_val'])
			elif self.config['comms']['inverter']['setpoint_dir'].lower() == 'discharge':
				self.config['comms']['inverter']['ref'].setDischarging(self.config['comms']['inverter']['setpoint_val'])
			else:
				self.config['comms']['inverter']['ref'].setCharging(0)

	def publish_setpoint(self, setpoint_type):
		try:
			tmp_values = self.config['MVC']['view'].get_values()

			tmp_values['window']['setpoint_type'] = setpoint_type
			tmp_values['window']['setpoint_indicator'] = f"{self.config['comms']['inverter']['setpoint_dir']} -> {self.config['comms']['inverter']['setpoint_val']} "

			self.config['MVC']['view'].update_values(tmp_values)

		except:
			pass

	def check_comm_battery(self):
		try:	
			self.config['comms']['battery']['connected'] = self.config['comms']['battery']['ref'].get_connection_status()
		except:
			self.config['comms']['battery']['connected'] = False

	def comm_battery(self, it):
		pass

	def comm(self):
		# error = False

		# while self.config['comms']['inverter']['comm']:
			# sleep(2)

			# conn_ok = self.config['comms']['inverter']['ref'].get_connection_status()

			# if conn_ok:
				# Si la conexión esta OK

		# Obtenemos valores anteriores
		tmp_values = self.config['MVC']['view'].get_values()

		# INVERTER
		try:
			# Leemos los valores de inverter
			tmp_dataset = self.config['comms']['inverter']['ref'].read()

			print(tmp_dataset)

			# Reemplazamos los valores de inverter recien leidos que no sean None
			for key, value in tmp_dataset['inverter'].items():
				if not value is None:
					tmp_values['inverter'][key] = value
		except:
			pass

		# BATTERY
		# try:
		# 	# Leemos los valores de battery
		# 	tmp_dataset = self.config['comms']['battery']['ref'].read()

		# 	# Reemplazamos los valores de inverter recien leidos que no sean None
		# 	for key, value in tmp_dataset['battery'].items():
		# 		if not value is None:
		# 			tmp_values['battery'][key] = value
		# except:
		# 	pass

			# Escribimos los valores actuales 
			self.config['MVC']['view'].update_values(tmp_values)

			# else:
			# 	# Si la conexión NO esta OK				
			# 	print("Connection lost...")

			# 	error = True
			# 	self.config['comms']['inverter']['comm'] = False

		# print("Exited COMM task!")

		# if error:
		# 	self.disconnect()

	# #################### CONTROL ####################
	def op_inverter(self, action = ''):
		if action == "run":
			self.run_inverter()
		elif action == "stop":
			self.stop_inverter()
			
	def run_inverter(self):
		print("Running inverter...")
		self.config['comms']['inverter']['ref'].connectGrid()

	def stop_inverter(self):
		print("Stopping inverter...")
		self.config['comms']['inverter']['ref'].disconnectGrid()

	# #################### MQTT ####################
	def mqtt_connect(self):
		self.mqtt = paho.Client('broker')
		self.mqtt.on_publish = self.mqtt_on_publish
		self.mqtt.connect(self.config['mqtt']['broker'], self.config['mqtt']['port'])

	def mqtt_on_publish(self):
		pass

	def mqtt_publish(self, data, topic = None):
		if topic is None:
			topic = self.config['mqtt']['topic']
			
		try:
			ret = self.mqtt.publish(topic, data)
		except Exception as e:
			print(f"Failed MQTT writing: {e}")


	# #################### TEST ####################
	def test_manager(self):
		print(f"{self.get_now()}: Test manager created!")

		self.test['checked'] = False
		self.test['running'] = False
		self.test['finished'] = False

		self.test['setpoint_val'] = 0
		self.test['setpoint_dir'] = 'rest'

		self.test['total_time'] = 0
		self.test['iterations'] = 0
		self.test['it'] = 0

		while self.config['app']['running']:
			# Check if test is running
			try:
				if self.test['running']:
					self.get_test_state()

					self.update_test_state()
			except:
				pass

			# Sleep
			thr = self.get_thread(name = 'test_manager')
			sleep(thr['timing'])


		print(f"{self.get_now()}: Test manager exited!")		

	def check_test(self, path = None):
    	# Comprbamos si hay algun test corriendo
		if not self.test['running']:
    		# Si no lo hay, comprobamos si el path es válido
			if not path is None:
    			# Guardamos el path
				self.test['file'] = path

				# Comprobamos si podemos cargar los steps del test
				check = {
					'file': self.test['file'],
					'ok': self.load_test_steps(verbose = False),
				}

				self.test['check'] = check

				# Inicializamos val y dir
				if self.test['check']['ok'] == 1:
					self.test['setpoint_val'] = 0
					self.test['setpoint_dir'] = 'rest'
				elif self.test['check']['ok'] == -1:
					self.test['setpoint_val'] = None
					self.test['setpoint_dir'] = None

				self.test['running'] = False
				self.test['finished'] = False

				# Send info to View
				self.update_test_state()
		else:
			self.config['MVC']['view'].set_message("Cannot check test while running another")

	def clear_test_steps(self):
		self.test['iterations'] = None
		self.test['n_steps'] = None
		self.test['base-time'] = None
		self.test['sleeping_value'] = None
		self.test['sleeping_type'] = None
		self.test['profile'] = None
		self.test['setpoint_val'] = None
		self.test['setpoint_dir'] = None

		self.test['starting_time'] = None
		self.test['total_steps'] = 0
		self.test['total_time'] = 0
		self.test['it'] = 0

	def load_test_steps(self, verbose = False):
		ret_val = None

		try:
			with open(self.test['file']) as jsonfile:
				test = json.load(jsonfile)

			# Intentamos leer el base_time (hour, minute), si no encontramos asignamos default
			try:
				self.test['base_time'] = test['base_time']
			except:
				self.test['base_time'] = 'hour'

			# Intentamos leer el sleeping_time / sleeping_value / sleeping_type, si no encontramos asignamos default (now, 0, charge)
			try:
				sleeping_time = test['sleeping_time']
			except:
				sleeping_time = -1

			try:
				self.test['sleeping_val'] = test['sleeping_val']
			except:
				self.test['sleeping_val'] = 0

			try:
				self.test['sleeping_dir'] = test['sleeping_dir'].lower()
			except:
				self.test['sleeping_dir'] = "rest"

			# Leemos los parámetros básicos
			self.test['name'] = test['name']

			self.test['iterations'] = test['iterations']

			self.test['n_steps'] = len(test['profile'])

			self.test['total_steps'] = self.test['iterations'] * self.test['n_steps']


			# Leemos y obtenemos cada step del profile
			self.test['profile'] = []

			if sleeping_time == "-1":
				dt_end = datetime.now()

				zero = 0
			else:
				# Asignamos el primer step como el SLEEPING
				step_time =datetime.now()
				step_val = self.test['sleeping_val']
				step_dir = self.test['sleeping_dir']

				zero = 1
				
				# Obtenemos los valores para el siguiente step
				req_hour = int(sleeping_time.split(":")[0])
				req_minute = int(sleeping_time.split(":")[1])

				current_now = datetime.now()
				current_year = datetime.now().date().year
				current_month = datetime.now().date().month
				current_day = datetime.now().date().day

				req_datetime = datetime(year = current_year, month = current_month, day = current_day, hour = req_hour, minute = req_minute)

				if req_datetime >= current_now:
					dt_end = req_datetime
				else:
					dt_end = datetime(year = current_year, month = current_month, day = current_day + 1, hour = req_hour, minute = req_minute)	

				tmp_profile = {}

				tmp_profile['iteration'] = 0
				tmp_profile['dt_ini'] = step_time
				tmp_profile['dt_end'] = dt_end
				tmp_profile['value'] = step_val
				tmp_profile['dir'] = step_dir

				self.test['profile'].append(tmp_profile)

			for i in range(zero, self.test['total_steps'] + zero):
				it = i % self.test['n_steps']

				step_time = test['profile'][it]['time']
				step_val = test['profile'][it]['val']
				step_dir = test['profile'][it]['dir'].lower()

				tmp_profile = {}

				tmp_profile['iteration'] = i
				tmp_profile['dt_ini'] = dt_end
				if self.test['base_time'] == "hour":
					tmp_profile['dt_end'] = tmp_profile['dt_ini'] + timedelta(hours = step_time)
				elif self.test['base_time'] == "minute":
					tmp_profile['dt_end'] = tmp_profile['dt_ini'] + timedelta(minutes = step_time)					
				elif self.test['base_time'] == "second":
					tmp_profile['dt_end'] = tmp_profile['dt_ini'] + timedelta(seconds = step_time)

				tmp_profile['val'] = step_val
				tmp_profile['dir'] = step_dir
				
				self.test['profile'].append(tmp_profile)

				dt_end = tmp_profile['dt_end']

			self.test['total_steps'] = self.test['total_steps'] + zero

			ret_val = 1

			if verbose:
				print(f"Name: {self.test['name']}")

				print(f"Base time: {self.test['base_time']}")

				print(f"Iterations: {self.test['iterations']}")
				print(f"N_steps: {self.test['n_steps']}")
				print(f"Total_steps: {self.test['total_steps']}")

				print(f"Sleeping time: {sleeping_time}")
				print(f"Sleeping value: {self.test['sleeping_val']}")
				print(f"Sleeping type: {self.test['sleeping_dir']}")

				for prof in self.test['profile']:
					print(prof)

		except Exception as e:
			ret_val = -1

			print("Error cause:")
			print(f"  - {e}")
		
		return ret_val

	def start_test(self):
		if self.test['check']['ok'] == 1:
			self.clear_test_steps()
			self.load_test_steps()

			self.test['starting_time'] = datetime.now()
			self.test['running'] = True
			self.test['finished'] = False
			
		elif self.test['check']['ok'] == -1:
			print('Cannot start test')
			self.test['running'] = False
			self.test['finished'] = False

		self.update_test_state()

	def stop_test(self):
		if self.test['check']['ok'] == 1:
			self.clear_test_steps()

			
			self.test['running'] = False
			self.test['finished'] = False
		elif self.test['check']['ok'] == -1:
			print('Cannot stop test')
			self.test['running'] = False
			self.test['finished'] = False

		self.update_test_state()

	def update_test_state(self):
		tmp_values = self.config['MVC']['view'].get_values()

		tmp_values['test']['path'] = self.test['check']['file']
		tmp_values['test']['ok'] = self.test['check']['ok']
		tmp_values['test']['running'] = self.test['running']
		tmp_values['test']['finished'] = self.test['finished']
		tmp_values['test']['total_time'] = self.test['total_time']
		tmp_values['test']['total_it'] = self.test['total_steps']
		tmp_values['test']['it'] = self.test['it']

		self.config['MVC']['view'].update_values(tmp_values)

	def get_test_state(self):
		now = datetime.now()

		it = 0
		for i, step in enumerate(self.test['profile']):
    		# Obtenemos los tiempos de cada iteración
			step_ini = step['dt_ini']
			step_end = step['dt_end']

			# Comprobamos si estamos dentro de alguno de los steps
			it = -1
			into_steps = False
			if (now >= step_ini) & (now < step_end):
    			# Si estamos, obtenemos step_val y step_dir
				into_steps = True

				step_val = step['val']
				step_dir = step['dir']

				it = i
				break
			
		# Si no estamos, cogemos sleeping_val y sleeping_dir
		if not into_steps:
			step_val = self.test['sleeping_val']
			step_dir = self.test['sleeping_dir']	

			it = -1

		# Comprobamos si hemos terminado el test
		self.test['finished'] = not into_steps

		# Volcamos val y dir
		self.test['setpoint_val'] = step_val
		self.test['setpoint_dir'] = step_dir

		# Actualizamos total_time e it
		self.test['total_time'] = now - self.test['starting_time']
		self.test['it'] = it
	
	# #################### APP ####################
	def run_app(self):
		self.config['MVC']['view'].run_app()

	def stop_app(self):
		self.config['MVC']['view'].set_message("Exiting...")

		self.config['app']['running'] = False

		self.kill_all_threads(verbose = True)

		self.disconnect()

		self.config['MVC']['view'].quit()



	# #################### AUX ####################
	def get_now(self):
		return datetime.now().strftime("%m/%d/%Y %H:%M:%S")




class inner_thread(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run     
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, event, arg):
		if event == 'call':
			return self.localtrace
		else:
			return None
 
	def localtrace(self, frame, event, arg):
		if self.killed:
			if event == 'line':
				raise SystemExit()
			return self.localtrace		

	def kill(self):
		self.killed = True			
