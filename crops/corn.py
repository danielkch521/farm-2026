from .crop import Crop

class Corn(Crop):
    def __init__(self):
        super().__init__('corn')

    def water_req(self):
        return "2 litres"
