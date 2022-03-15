from model.model import Model
from view.view import View
from controller.controller import Controller


if __name__ == "__main__":
	# MVC
	model = Model()
	view = View()
	controller = Controller()

	data = {}
	data['model'] = model
	data['view'] = view
	data['controller'] = controller

	controller.set_mvc_refs(data)	
	controller.set_scale({'abs': 0.8})	
	controller.run_app()




