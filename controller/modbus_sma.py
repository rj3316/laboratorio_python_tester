from controller.modbus import Modbus
from pyModbusTCP.utils import word_list_to_long, long_list_to_word

from datetime import datetime

from math import floor

class sma(Modbus):
	def __init__(self, *args) -> None:
		super().__init__(*args)

		self.n_reg_base = 2

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

			# Status / Operation
			try:
				tmp_data = self.getOperation()[0]
				# tmp_data = self.getStatus()[0]
			except:
				tmp_data = None
			tmp_dataset['inverter']['status'] = tmp_data

			tmp_dataset['inverter']['running'] = (tmp_data == 'RUN')

			# Bat Status
			try:
				tmp_data = self.getBatteryState()[0]
			except:
				tmp_data = None
			tmp_dataset['inverter']['bat_status'] = tmp_data

			# Bat SoC
			try:
				tmp_data = self.getSoC()[0]
			except:
				tmp_data = None
			tmp_dataset['inverter']['bat_soc'] = tmp_data	

			# Bat Voltage
			try:
				tmp_data = self.getBatteryVoltage()[0]
			except:
				tmp_data = None
			tmp_dataset['inverter']['bat_voltage'] = tmp_data	


			# Bat Current
			try:
				tmp_data = self.getBatteryCurrent()[0]
			except:
				tmp_data = None
			tmp_dataset['inverter']['bat_current'] = tmp_data	

			# Power
			try:
				tmp_data = self.getPower()[0]
				tmp_dataset['inverter']['power_3'] = tmp_data[0]
				tmp_dataset['inverter']['power_r'] = tmp_data[1]
				tmp_dataset['inverter']['power_s'] = tmp_data[2]
				tmp_dataset['inverter']['power_t'] = tmp_data[3]
			except:
				tmp_dataset['inverter']['power_3'] = None
				tmp_dataset['inverter']['power_r'] = None
				tmp_dataset['inverter']['power_s'] = None
				tmp_dataset['inverter']['power_t'] = None

			ret_val = tmp_dataset
		else:
			ret_val = None
		
		return ret_val

	def read_register(self, address, n_reg = -1, signed = False, verbose = False):
		try:
			if n_reg == -1:
					n_reg = self.n_reg_base

			if n_reg % self.n_reg_base != 0:
				print("Not valid number of registers")

				result = None
			else:
				# Get the current time and read the register
				now = datetime.now()
				read_address = address + self.base
				raw = self.client.read_holding_registers(read_address, n_reg)

				if verbose:
					print(f" \n* Reading holdings on {read_address}: {raw}")

				if not raw is None:
					if n_reg == self.n_reg_base:
						if not signed:
							result = word_list_to_long(raw)[0]
						else:
							result = self.transformSignedData(raw)
					else:
						n_it = floor(n_reg / self.n_reg_base)

						result = []
						for n in range(n_it):
							i = self.n_reg_base * n

							data = []
							data.append(raw[i])
							data.append(raw[i+1])

							if not signed:
								tmp_res = word_list_to_long(data)[0]
							else:
								tmp_res = self.transformSignedData(data)

							result.append(tmp_res)
				else:
					result = None

				success = True
		except:
			now = datetime.now()
			result = []

			success = False

		# Writing log
		message = f"READ {address} {n_reg} bytes -> {result} (Succes {success})"
		self.write_log(message)

		return result		

	def transformSignedData(self, raw):
		if ((65535 - raw[0]) > raw[0]):
			sign = raw[0]
			value = raw[1] + 65535*sign
		else:
			sign = 65536 - raw[0]
			value = raw[1] - 65535*sign
		return value

	def writeRegister(self, address, value, verbose = False):
		if verbose:
			print(f"    Writing power: {value}...")

		# Get the 2complement if value is negative
		if(value < 0):
			w_value = -(-value - (1 << 32))
			neg=True
		else:
			w_value=value
			neg=False

		# Get the current time and write the register
		now = datetime.now()
		data = long_list_to_word([w_value])

		if neg:
			data[0] = 65535
		else:
			data[0] = 0

		# Transmit the data and write the result to the log file
		writeOK = self.client.write_multiple_registers(address + self.base, data)

		# Writing log
		message = f"WRITE {address} -> {data} ({writeOK})"
		self.write_log(message)
				
		return writeOK

	# Specific methods
	def getGeneralInfo(self): # 30053 / 30055 / 30057
		in_info = self.read_register(30053, 6)

		in_model = in_info[0]
		in_manuf = in_info[1]
		serial = in_info[2]

		if in_model == 9331: # 0x2473
			model = "Sunny Island 3.0M (SI 3.0M - 12)"
		elif in_model == 9332: # 0x2474
			model = "Sunny Island 4.4M (SI 4.4M - 12)"
		elif in_model == 9333: # 0x2475
			model = "Sunny Island 6.0H (SI 6.0H - 12)"
		elif in_model == 9334: # 0x2476
			model = "Sunny Island 8.0H (SI 8.0H - 12)"
		elif in_model == 9374: # 0x249E
			model = "Sunny Island 4.4M (SI 4.4M - 13)"
		elif in_model == 9375: # 0x249F
			model = "Sunny Island 6.0H (SI 6.0H - 13)"
		elif in_model == 9376: # 0x24A0
			model = "Sunny Island 8.0H (SI 8.0H - 13)"
		elif in_model == 9386: # 0x24AA
			model = "Sunny Island 5.0H (SI 5.0H - 13)"
		else:
			model = "Unknown model"

		if in_manuf == 461: #0x01CD
			manuf = "SMA"
		else:
			manuf = "Unknown manufacturer"

		info = []
		info.append(manuf)
		info.append(model)
		info.append(serial)

		return info

	def getStatus(self): # 30201
		status = self.read_register(30201)
		if(status == 35): # 0x0023
			result = 'FAULT'
		elif(status == 303): # 0x012F
			result = 'OFF'
		elif(status == 307): # 0x0133
			result = 'OK'
		elif(status == 455): # 0x01C7
			result = 'WARNING'
		else:
			result = ''

		return result, datetime.now()

	def getPower(self): # 30775 / 30777 / 30779
		return self.read_register(30775, n_reg = 8, signed = True), datetime.now()

	def getBatteryCurrent(self): # 30843
		return self.read_register(30843, signed = True) / 1000.0, datetime.now()

	def getSoC(self): #30845
		return self.read_register(30845), datetime.now()

	def getBatteryTemperature(self): # 30849
		return self.read_register(30849, signed = True), datetime.now()

	def getBatteryVoltage(self): # 30851
		return  self.read_register(30851) / 100.0, datetime.now()

	def getBatteryState(self): # 30955
		state = self.read_register(30955)

		if state == 2292: # 0x08F4
			result = "BatChaStt"
		elif state == 2293: #0x08F5
			result = "BatDschStt"
		else:
			result = "NaNStt"

		return result

	def getOperation(self): # 40029
		tmp_operation = self.read_register(40029)

		if tmp_operation==303: # 0x012F
			operation="OFF"
		elif tmp_operation==569: # 0x0239
			operation="RUN"
		elif tmp_operation==1295: # 0x050F
			operation="STANDBY"
		elif tmp_operation==1795: # 0x0703
			operation="LOCKED"
		else:
			operation="UNKNOWN"

		return operation

	def getBatteryParams(self):
		in_info = self.read_register(40079, 12)

		print(f"Battery params: {in_info}")




	def setPowerLimit(self, powerLim = 100000):
		return self.writeRegister(40915, powerLim)

	def setSocLowLimit(self, socLim = 10):
		return self.writeRegister(40707, socLim)

	def setSocLowRecovery(self, socRecovery = 15):
		return self.writeRegister(40705, socRecovery)

	def setCharging(self, power):
		self.setPowerReference(-abs(power))

	def setDischarging(self, power):
		self.setPowerReference(abs(power))

	def setPowerReference(self, power):
		return self.writeRegister(40149, power)


	def setCommTimeout(self, timeout = 1800):
		return self.writeRegister(40195, timeout)

	def connectGrid(self):
		return self.writeRegister(40009, 1467)

	def disconnectGrid(self):
		return self.writeRegister(40009, 381)

	def enableDynamicReference(self):
		return self.writeRegister(44029, 303)

	def disableDynamicReference(self):
		return self.writeRegister(44029, 308)

	def enablePowerReference(self):
		c1 = self.writeRegister(40151, 802)

		if c1:
			c2 = self.writeRegister(40210, 1079)
		else:
			c2 = False
			
		return c1 & c2

	def disablePowerReference(self):
		return self.writeRegister(40151, 803)

	def enable_writing(self):
		self.enablePowerReference()
		self.enableDynamicReference()
		self.setPowerLimit()
		self.setSocLowLimit(8)
		self.setSocLowRecovery(10)
			   

