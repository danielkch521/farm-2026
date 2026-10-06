from .base_animal import BaseAnimal

class Sheep(BaseAnimal):
    def make_noise(self):
        return f"{self.name} says Baa!"
