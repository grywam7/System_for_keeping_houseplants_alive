import ujson
import os
import machine
from models.plant import Plant


class PlantRepo:
    def _filename(self, pot_index: int) -> str:
        return "plant_{}.json".format(pot_index)

    async def load(self, pot_index: int) -> Plant:
        try:
            with open(self._filename(pot_index), "r") as f:
                data = ujson.load(f)
            return Plant.from_dict(data)
        except Exception as e:
            print("Błąd odczytu rośliny {}:".format(pot_index), e)
            return None

    async def save(self, plant: Plant) -> None:
        try:
            with open(self._filename(plant.pot_index), "w") as f:
                ujson.dump(plant.to_dict(), f)
        except Exception as e:
            print("Błąd zapisu rośliny {}:".format(plant.pot_index), e)

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


# class PlantTypeRepo:
# to do


class Log:
    async def add(
        self, name: str, message: str, additional_info: dict
    ) -> None:  ## zrobić żeby dodawała na koniec pliku
        try:
            current_log = self.load_all
            if current_log.__len__ > 20:
                current_log.pop
            current_log.append(
                {
                    "name": name,
                    "message": message,
                    "info": additional_info,
                    "timestamp": machine.RTC().datetime()[:7],
                },
            )
            with open("/log.json", "w") as f:
                ujson.dump(
                    current_log,
                    f,
                )
        except Exception as e:
            print("Błąd zapisu loga!? {}:".format(name + ", " + message), e)

    async def load_all(self) -> list:
        try:
            with open("/log.json", "r") as f:
                return ujson.load(f)
        except Exception as e:
            print("Błąd odczytu loga:", e)
