import ujson
import os
from models.plant_types import Plant


class PlantRepo:
    def _filename(self, plant_id: int) -> str:
        return "plant_{}.json".format(plant_id)

    async def load(self, plant_id: int) -> Plant:
        try:
            with open(self._filename(plant_id), "r") as f:
                data = ujson.load(f)
            return Plant.from_dict(data)
        except Exception as e:
            print("Błąd odczytu rośliny {}:".format(plant_id), e)
            return None

    async def save(self, plant: Plant) -> None:
        try:
            with open(self._filename(plant.plant_id), "w") as f:
                ujson.dump(plant.to_dict(), f)
        except Exception as e:
            print("Błąd zapisu rośliny {}:".format(plant.plant_id), e)

    async def load_all(self) -> list:
        plants = []
        try:
            files = os.listdir()  # list files in the current directory
            for filename in files:
                if filename.startswith("plant_") and filename.endswith(".json"):
                    with open(filename, "r") as f:
                        data = ujson.load(f)
                    plants.append(Plant.from_dict(data))
        except Exception as e:
            print("Błąd odczytu wszystkich roślin:", e)
        return plants

    async def save_all(self, plants: list) -> None:
        # Save each plant individually
        for plant in plants:
            await self.save(plant)
