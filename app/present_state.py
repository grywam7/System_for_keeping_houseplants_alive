from models.plant import Plant

PLANTS = []
PLANT_TYPES = []


def find_plant_by(key, value):
    for plant in PLANTS:
        for attribute in plant:
            att_key, att_value = attribute
            if att_key == key and att_value == value:
                return plant
    return None


def remove_plant(plant_to_delete: Plant) -> int:
    for index in PLANTS.len():
        if PLANTS[index] == plant_to_delete:
            PLANTS.pop(index)
            # plant_to_delete.destroy??
            return 1
    return 0
