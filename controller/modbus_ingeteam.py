from controller.modbus import Modbus

from datetime import datetime
import numpy as np


class ingeteam(Modbus):
	def __init__(self, *args) -> None:
		super().__init__(*args)

		self.n_reg_base = 1

		self.base = 0

		sim = False

		try:
			if sim:
				self.base = -2
			else:
				if self.base <= 0:
					self.base = 0
				if self.base >= 1:
					self.base = 1
		except:
			pass  

	def read(self):
		ret_val = None

		if self.get_connection_status():
			tmp_dataset = self.create_dataset()

			tmp_dataset['timestamp'] = datetime.now()

			# General info
			tmp_dataset['inverter']['manufacturer'] = 'Ingeteam'
			tmp_dataset['inverter']['model']        = 'unknown'
			tmp_dataset['inverter']['serial']       = 'unknown'

			try:
				# Data package 1
				tmp_data = self.get_pack_1()

				# Inverter Datetime
				tmp_dataset['inverter']['datetime'] = datetime(year = tmp_data[0], month = tmp_data[1], day = tmp_data[2], hour = tmp_data[3], minute = tmp_data[4])

				# Status
				if tmp_data[20] == 0:
					tmp_dataset['inverter']['status'] = 'Not ready to connect'
					tmp_dataset['inverter']['running'] = False
				elif tmp_data[20] == 1:
					tmp_dataset['inverter']['status'] = 'Waiting to connect'
					tmp_dataset['inverter']['running'] = False
				elif tmp_data[20] == 2:
					tmp_dataset['inverter']['status'] = 'Connected to the grid'
					tmp_dataset['inverter']['running'] = True
				else:
					tmp_dataset['inverter']['status'] = 'Unknown'
					tmp_dataset['inverter']['running'] = False
					
						
				tmp_dataset['inverter']['alarms'] = None 

				tmp_current_r = (tmp_data[21] / 100.0)
				tmp_current_s = (tmp_data[22] / 100.0)
				tmp_current_t = (tmp_data[23] / 100.0)

				tmp_voltage_r = (tmp_data[24] / 10.0)
				tmp_voltage_s = (tmp_data[25] / 10.0)
				tmp_voltage_t = (tmp_data[26] / 10.0)

				tmp_cos_fi = (self.transformSignedData(tmp_data[31]) / 1000.0)

				# Power
				tmp_dataset['inverter']['power_3'] = (self.transformSignedData(tmp_data[29]) * 10)
				tmp_dataset['inverter']['power_r'] = round(tmp_current_r * tmp_voltage_r * tmp_cos_fi, 2)
				# tmp_dataset['inverter']['power_r'] = tmp_data[30]/3.0
				tmp_dataset['inverter']['power_s'] = round(tmp_current_s * tmp_voltage_s * tmp_cos_fi, 2)
				# tmp_dataset['inverter']['power_s'] = tmp_data[30]/3.0
				tmp_dataset['inverter']['power_t'] = round(tmp_current_t * tmp_voltage_t * tmp_cos_fi, 2)
				# tmp_dataset['inverter']['power_t'] = tmp_data[30]/3.0

				tmp_dataset['inverter']['bat_voltage'] = tmp_data[33]
				tmp_dataset['inverter']['bat_current'] = (self.transformSignedData(tmp_data[32]) / 100.0)
				tmp_dataset['inverter']['bat_power'] = (self.transformSignedData(tmp_data[35]) / 10.0)
			except:
				pass
			
			try:
				# Data package 2
				tmp_data = self.get_pack_2()

				if tmp_data[0] == 0:
					tmp_bat_status = 'Disconnected'
				elif tmp_data[0] == 1:
						tmp_bat_status = 'Standby'
				elif tmp_data[0] == 2:
						tmp_bat_status = 'Discharge'
				elif tmp_data[0] == 3:
						tmp_bat_status = 'Charge'
				elif tmp_data[0] == 4:
						tmp_bat_status = 'Absortion'
				elif tmp_data[0] == 5:
					tmp_bat_status = 'Float'
				tmp_dataset['inverter']['bat_status'] = tmp_bat_status
				
				tmp_dataset['inverter']['bat_soc']    = tmp_data[6]
			except:
				pass

			ret_val = tmp_dataset
		else:
			ret_val = None

		return ret_val

	def read_register(self, address, n_reg = -1, signed = False, verbose = False):
		try:
			if n_reg == -1:
				n_reg = self.n_reg_base

			if not (n_reg % self.n_reg_base == 0):
				print("Not valid number of registers")

				result = None    		
			else:
				# Get the current time and read the register
				now = datetime.now()
				read_address = address + self.base
				raws = self.client.read_input_registers(read_address, n_reg)

				if verbose:
					print(f" \n* Reading inputs on {read_address}: {raws} ({type(raws)})")

				result = []
				if not raws is None:
					for raw in raws:
						if not signed:
							result.append(raw)
						else:
							result.append(self.transformSignedData(raw))

				success = True
		except:
			now = datetime.now()
			result = []

			success = False
						
		# Writing log
		message = f"READ {address} {n_reg} bytes -> {result} (Succes {success})"
		self.write_log(message)

		return result, now					

	def write_register(self, data, addresss = 1000):
		address = 1000 + self.base

		writeOK = self.client.write_multiple_registers(address, data)

		# Writing log
		message = f"WRITE {address} -> {data} ({writeOK})"
		self.write_log(message)

		return writeOK

	def get_pack_1(self):
		return self.read_register(address = 0, n_reg = 55)[0]

	def get_pack_2(self):
		return self.read_register(address = 1008, n_reg = 7)[0]

	def connectGrid(self):
		data = []
		data.append(6)
		data.append(0)
		data.append(0)

		print(f"Connecting to grid... {data}")
		return self.write_register(data)

	def disconnectGrid(self):
		data = []
		data.append(5)
		data.append(0)
		data.append(0)

		print(f"Disconnecting from grid... {data}")
		return self.write_register(data)

	def setCharging(self, power):
		tmp_power = int(32767 * power / 100e3)
		
		# Limitamos la referencia
		tmp_power = min([tmp_power, 32767])

		data = []
		data.append(28)
		data.append(tmp_power)
		data.append(0)
		
		return self.write_register(data)

	def setDischarging(self, power):
		tmp_power = int(32767 * power / 100e3)

		# Limitamos la referencia
		tmp_power = min([tmp_power, 32767])
		
		data = []
		data.append(29)
		data.append(tmp_power)
		data.append(0)

		return self.write_register(data)
					
	def enable_writing(self):
		pass
	
	def transformSignedData(self, input = 0):
		return np.int16(input)