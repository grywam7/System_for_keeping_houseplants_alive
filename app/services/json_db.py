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
                Log.add(
                    "json_db - PlantRepo",
                    f"Roślina {pot_index} odczytana pomyślnie",
                )
            return Plant.from_dict(data)
        except Exception as e:
            Log.add(
                "json_db - PlantRepo", f"Błąd odczytu rośliny {pot_index}", f"error:{e}"
            )
            return None

    async def save(self, plant: Plant) -> None:
        try:
            with open(self._filename(plant.pot_index), "w") as f:
                ujson.dump(plant.to_dict(), f)
        except Exception as e:
            Log.add(
                "json_db - PlantRepo",
                f"Błąd zapisu rośliny {plant.pot_index}",
                f"error:{e}",
            )
        Log.add(
            "json_db - PlantRepo",
            f"Roślina {plant.pot_index} zapisana pomyślnie",
        )

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
            Log.add("json_db - PlantRepo", "Błąd odczytu wszystkich roślin", str(e))
        return plants

    async def save_all(self, plants: list) -> None:
        # Save each plant individually
        for plant in plants:
            await self.save(plant)
            Log.add(
                "json_db - PlantRepo",
                f"Roślina {plant.pot_index} zapisana pomyślnie",
            )


# class PlantTypeRepo:
# to do


class Log:
    @classmethod
    def load_all(self) -> list:
        try:
            with open("../log.json", "r") as f:
                return ujson.load(f)
        except Exception as e:
            print("Błąd odczytu loga:", e)

    @classmethod
    def add(self, name: str, message: str, additional_info: dict = {}) -> None:
        try:
            print(
                "name: ",
                name,
                " | message: ",
                message,
                "| info: ",
                ujson.dumps(additional_info),
            )
            current_log = self.load_all()

            if len(current_log) > 20:
                current_log.pop(0)

            current_log.append(
                {
                    "name": name,
                    "message": message,
                    "info": additional_info,
                    "timestamp": machine.RTC().datetime()[:7],
                }
            )
            with open("../log.json", "w") as f:
                ujson.dump(current_log, f)
        except Exception as e:
            print(f"Błąd zapisu loga!? {name + ', ' + message}:", e)
