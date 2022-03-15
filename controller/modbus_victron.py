from controller.modbus import Modbus

from datetime import datetime

from math import floor, pow


class victron(Modbus):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        pass