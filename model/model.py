# MODEL

class Model():
	def __init__(self) -> None:
		self.config = {}

		self.create_config()

	def create_config(self):
		self.config = {
			'MVC': {},
		}

		# MVC REF
		if True:
			self.config['MVC']['components'] = ['model', 'view', 'controller']
			self.config['MVC']['model'] = None
			self.config['MVC']['view'] = None
			self.config['MVC']['controller'] = None	


	def set_mvc_refs(self, data, verbose = False):
		for mvc in data:
			if mvc in self.config['MVC']['components']:
				if mvc == 'model':
					self.config['MVC'][mvc] = self
				else:
					self.config['MVC'][mvc] = data[mvc]

		if verbose:
			print("\\nModel MVC refs changed!")
			print(f"  - Model: 		{self.config['MVC']['model']}")
			print(f"  - View: 		{self.config['MVC']['view']}")
			print(f"  - Controller: {self.config['MVC']['controller']}")            