from models.plant import Plant


plants = []
plant_types = []


def find_plant_by(key, value):
    for plant in plants:
        for attribute in plant:
            att_key, att_value = attribute
            if att_key == key and att_value == value:
                return plant
    return None


def remove_plant(plant_to_delete: Plant) -> int:
    for index in plants.len():
        if plants[index] == plant_to_delete:
            plants.pop(index)
            # plant_to_delete.destroy??
            return 1
    return 0
