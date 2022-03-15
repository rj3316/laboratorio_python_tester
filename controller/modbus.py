from pyModbusTCP.client import ModbusClient

from datetime import datetime

class Modbus():
	def __init__(self, *args) -> None:
		self.config = {}
		self.create_config()

		data = {
			'ip': args[0],
			'port': args[1],
			'uid': args[2],
			'timeout': 2,
			'manufacturer': args[3],
		}		
		self.set_comms(data)

		self.connect()        
		
	def create_config(self):
		self.config = {
			'MVC': {},
			'comms': {},
		}

		# MVC
		self.config['MVC']['components'] = ['model', 'view', 'controller']
		self.config['MVC']['model'] = None
		self.config['MVC']['view'] = None
		self.config['MVC']['controller'] = None

		# COMMS
		self.config['comms']['ip'] = None
		self.config['comms']['port'] = None
		self.config['comms']['uid'] = None
		self.config['comms']['timeout'] = 3
		self.config['comms']['manufacturer'] = None

		# LOG
		self.log = None

	def create_dataset(self):
		dataset = {
			'timestamp': None,
			'inverter': {},
			'battery': {},
		}

		dataset['inverter']['manufacturer'] = None
		dataset['inverter']['model']        = None	
		dataset['inverter']['serial']       = None

		dataset['inverter']['datetime'] = None

		dataset['inverter']['status'] = None
		dataset['inverter']['running'] = None

		dataset['inverter']['alarms'] = None 

		dataset['inverter']['power_3'] = None
		dataset['inverter']['power_r'] = None
		dataset['inverter']['power_s'] = None
		dataset['inverter']['power_t'] = None

		dataset['inverter']['bat_status']  = None
		dataset['inverter']['bat_soc']     = None
		dataset['inverter']['bat_voltage'] = None
		dataset['inverter']['bat_current'] = None
		dataset['inverter']['bat_power']   = None

		dataset['battery']['manufacturer'] = None
		dataset['battery']['model']        = None	
		dataset['battery']['serial']       = None

		dataset['battery']['status']       = None
		dataset['battery']['running']      = None

		dataset['battery']['voltage']      = None
		dataset['battery']['current']      = None
		dataset['battery']['soc']          = None
		dataset['battery']['ch_current']   = None
		dataset['battery']['dsch_current'] = None
		dataset['battery']['ch_voltage']   = None
		dataset['battery']['dsch_voltage'] = None

		return dataset

	def set_mvc_refs(self, data, verbose = False):
		for mvc in data:
			if mvc in self.config['MVC']['components']:
				self.config['MVC'][mvc] = data[mvc]

		if verbose:
			print("Controller MVC refs changed!")
			print(f"  - Model: 		{self.config['MVC']['model']}")
			print(f"  - View: 		{self.config['MVC']['view']}")
			print(f"  - Controller: {self.config['MVC']['controller']}")

	def set_comms(self, data):
    	# IP, PORT, UID
		for key in data:
			try:
				self.config['comms'][key] = data[key]
			except:
				pass

	def show_comms(self):
		print("\nModbus comms:")
		print(f"  - Ip: {self.config['comms']['ip']} / {type(self.config['comms']['ip'])}")
		print(f"  - Port: {self.config['comms']['port']} / {type(self.config['comms']['port'])}")
		print(f"  - UID: {self.config['comms']['uid']} / {type(self.config['comms']['uid'])}")			

	# Method that starts the connection
	def connect(self):
		ip = self.config['comms']['ip']
		port = self.config['comms']['port']
		uid = self.config['comms']['uid']
		timeout = self.config['comms']['timeout']

		# Connect to the specified server
		self.client = ModbusClient(host = ip, port = port, unit_id = uid, timeout = timeout)

		if(self.client.open()):
			message='Connection established with ' + ip + ':' + str(port)
			print('Connection established with ' + ip + ':' + str(port))
		else:
			message='Connection could not be established...'
			print('Connection could not be established...')

		# Open log file
		self.create_log()

	# Method that terminates the connection
	def disconnect(self):
		# self.log.close()
		if(self.client.close()):
			print('Connection closed succesfully')

	def get_connection_status(self):
		return self.client.is_open()
    			
	def read(self):
		pass

	def read_register(self):
		pass

	def write(self):
		pass

	def write_register(self):
		pass

	def connectGrid(self):
		# Polymorphic method
		pass

	def disconnectGrid(self):
		# Polymorphic method
		pass

	def setCharging(self):
		# Polymorphic method
		pass

	def setDischarging(self):
		# Polymorphic method
		pass

	# LOG
	def create_log(self):
		log_name = self.config['comms']['ip'].replace('.', '') + '_' + str(self.config['comms']['port'])
		self.log = open(log_name + '.log', 'a')

		self.log.write(f"\n{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} -> {self.config['comms']['manufacturer']} - New connection stablished with {self.config['comms']['ip']}:{self.config['comms']['port']} - UID: {self.config['comms']['uid']}\n")

	def write_log(self, message):
		new_message = f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} ->   "

		new_message += message
		new_message += '\n'

		self.log.write(new_message)

		# Flush the log file and return the result
		self.log.flush()

