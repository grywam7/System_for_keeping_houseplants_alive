from models.plant import Plant


plants = []
plant_types = []


def find_plant_by(key: str, value) -> Plant | None:
    for plant in plants:
        if getattr(plant, key, None) == value:
            return plant

        # if plant.to_dict().get(key) == value:
        # return plant
    return None


def remove_plant(plant_to_delete: Plant) -> int:
    for index in plants.len():
        if plants[index] == plant_to_delete:
            plants.pop(index)
            # plant_to_delete.destroy??
            return 1
    return 0
