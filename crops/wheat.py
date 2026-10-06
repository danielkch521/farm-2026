from .crop import Crop

class Wheat(Crop):
    def __init__(self):
        super().__init__('wheat')

    def water_req(self):
        return "3 litres"
