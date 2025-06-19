class PlantType:
    def __init__(self, name: str, watering_hour: int, ilumination_time: int):
        self.name = name
        self.watering_hour = watering_hour
        self.ilumination_time = ilumination_time

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict) -> "PlantType":
        return cls(**data)
