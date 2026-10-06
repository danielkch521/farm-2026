class Crop:
    def __init__(self, name):
        self.name = name

    def grow(self):
        return f"The {self.name} crop is growing."

    def water_needs(self):
        return f"{self.name} crop needs {self.water_req()} water."

    def water_req(self):
        raise NotImplementedError("Subclasses must implement water_req method")
