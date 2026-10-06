from .crop import Crop

class Rice(Crop):
    def __init__(self):
        super().__init__('rice')

    def water_req(self):
        return "4 litres"
