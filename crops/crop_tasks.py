
class WaterCrop:
    def __init__(self, water_amount):
        self.water_amount = water_amount

    def __call__(self, crop):
        return f"{crop.name} received {self.water_amount} liters of water."

class FertilizeCrop:
    def __init__(self, fertilizer_type, amount):
        self.fertilizer_type = fertilizer_type
        self.amount = amount

    def __call__(self, crop):
        return f"{crop.name} was fertilized with {self.amount} kg of {self.fertilizer_type}."

class HarvestCrop:
    def __init__(self, tonnes):
        self.tonnes = tonnes

    def __call__(self, crop):
        return f"{self.tonnes} tonnes of {crop.name} were harvested."

