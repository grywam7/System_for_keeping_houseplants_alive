class PlantType:
    def __init__(self, name: str, water_requirements: int, light_requirements: int):
        self.name = name
        self.water_requirements = water_requirements  # np. minimalna ilość wody [ml] lub odstęp między podlaniami
        self.light_requirements = light_requirements  # np. ilość godzin światła

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


class Plant:
    def __init__(
        self,
        plant_id: int,
        plant_type: PlantType,
        last_watered: float,
        last_illuminated: float,
    ):
        self.plant_id = plant_id
        self.plant_type = plant_type
        self.last_watered = last_watered  # np. znacznik czasu ostatniego podlewania
        self.last_illuminated = (
            last_illuminated  # np. znacznik czasu ostatniego doświetlenia
        )

    def to_dict(self) -> dict:
        return {
            "plant_id": self.plant_id,
            "plant_type": self.plant_type.to_dict(),
            "last_watered": self.last_watered,
            "last_illuminated": self.last_illuminated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Plant":
        plant_type_data = data.get("plant_type", {})
        plant_type = PlantType.from_dict(plant_type_data)
        return cls(
            plant_id=data.get("plant_id"),
            plant_type=plant_type,
            last_watered=data.get("last_watered", 0),
            last_illuminated=data.get("last_illuminated", 0),
        )
