from .crop import Crop

class Potato(Crop):
    def __init__(self):
        super().__init__('potato')

    def water_req(self):
        return "1 litre"
