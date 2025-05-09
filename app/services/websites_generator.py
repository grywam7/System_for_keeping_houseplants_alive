from services.json_db import PlantRepo

# from services.json_db import PlantTypeRepo
from models.plant import Plant


def generate_plants_cards(plants: list) -> str:
    html_header = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Plant Cards</title>
  <style>
    .card-container {
      display: flex;
      flex-wrap: wrap;
      gap: 1em;
    }
    table {
      margin: 1em;
    }
    table, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
  </style>
</head>
<body>
<h1>Plant Cards</h1>
<div class="card-container">
"""
    html_footer = """
</div>
</body>
</html>
"""
    body = ""
    for plant in plants:
        info = plant.to_dict()
        card = '<div class="card"><table>'
        for key, value in info.items():
            card += f"<tr><td>{key}</td><td><strong>{value}</strong></td></tr>"
        card += "</table>"
        body += card

    return html_header + body + html_footer


# def generate_plant_site(plant: Plant) -> str:
# TODO: implement this function
# This function should generate a detailed HTML page for a single plant
# using the plant's data.
