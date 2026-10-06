from .equipment import Equipment

class Sprinkler(Equipment):
    def __init__(self, name, litres_per_minute):
        super().__init__(name)
        self.litres_per_minute = litres_per_minute

    def operate(self):
        return f"The {self.name} is spraying {self.litres_per_minute} litres per minute."
