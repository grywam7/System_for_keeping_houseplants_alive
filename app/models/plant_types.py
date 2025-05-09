class PlantType:
    def __init__(self, name: str, watering_hour: int, ilumination_time: int):
        self.name = name
        self.watering_hour = watering_hour
        self.ilumination_time = ilumination_time

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "water_requirements": self.water_requirements,
            "light_requirements": self.light_requirements,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlantType":
        return cls(
            name=data.get("name"),
            water_requirements=data.get("water_requirements"),
            light_requirements=data.get("light_requirements"),
        )
